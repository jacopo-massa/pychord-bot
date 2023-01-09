import telebot
import pychord
import os
import logging

from messages import *

# get bot token as environment variable
BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="MARKDOWN")
logger = telebot.logger
telebot.logger.setLevel(logging.INFO) # Outputs debug messages to console.

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, WELCOME_MESSAGE)

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, HELP_MESSAGE)

@bot.message_handler(commands=['chord'])
def send_chord(message):
    bot.send_message(message.chat.id, CHORD_MESSAGE)

@bot.message_handler(commands=['compose'])
def send_compose(message):
    bot.send_message(message.chat.id, COMPOSE_MESSAGE)

@bot.message_handler(regexp="\[\S+\]")
def send_chord_analysis(message):
    ch = pychord.Chord(message.text[1:-1])
    text = get_chord_analysis_message(ch)
    bot.reply_to(message, f"````{text}```", parse_mode="MARKDOWN")


if __name__ == '__main__':
    bot.infinity_polling(skip_pending=True)
else:
    pass