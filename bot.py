import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from tinydb import TinyDB, Query

API_KEY = os.getenv("API_KEY")
bot = telebot.TeleBot(API_KEY)
db = TinyDB('db.json')
User = Query()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Welcome to InstaMatch!\nLet’s set up your profile.")
    ask_name(message)

def ask_name(message):
    msg = bot.send_message(message.chat.id, "What is your name?")
    bot.register_next_step_handler(msg, save_name)

def save_name(message):
    user_id = message.from_user.id
    db.upsert({'id': user_id, 'name': message.text}, User.id == user_id)
    ask_age(message)

def ask_age(message):
    msg = bot.send_message(message.chat.id, "How old are you?")
    bot.register_next_step_handler(msg, save_age)

def save_age(message):
    user_id = message.from_user.id
    db.update({'age': message.text}, User.id == user_id)
    ask_gender(message)

def ask_gender(message):
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("Male", callback_data="gender_Male"),
        InlineKeyboardButton("Female", callback_data="gender_Female"),
        InlineKeyboardButton("Other", callback_data="gender_Other")
    )
    bot.send_message(message.chat.id, "What is your gender?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("gender_"))
def handle_gender(call):
    gender = call.data.split("_")[1]
    user_id = call.from_user.id
    db.update({'gender': gender}, User.id == user_id)
    bot.send_message(call.message.chat.id, f"Saved gender: {gender}")
    ask_bio(call.message)

def ask_bio(message):
    msg = bot.send_message(message.chat.id, "Write a short bio about yourself:")
    bot.register_next_step_handler(msg, save_bio)

def save_bio(message):
    user_id = message.from_user.id
    db.update({'bio': message.text}, User.id == user_id)
    ask_instagram(message)

def ask_instagram(message):
    msg = bot.send_message(message.chat.id, "What’s your Instagram username? (without @)")
    bot.register_next_step_handler(msg, save_instagram)

def save_instagram(message):
    user_id = message.from_user.id
    db.update({'instagram': message.text}, User.id == user_id)
    bot.send_message(message.chat.id, "Profile setup complete! Type /find to discover people.")

bot.polling()