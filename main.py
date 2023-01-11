import telebot
import pychord
import os
import re
import logging
import requests

from telebot import types
from messages import *
from analysis import *

# get environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
IMGBUN_API_KEY = os.getenv('IMGBUN_API_KEY')

CHORD_REGEX = "\[\S+\]"
COMPOSE_REGEX = "\{([A-Z#b]|\s)+\}"

CHORD_URL = "https://www.scales-chords.com/api/scapi.1.3.php"
THUMBNAIL_URL = f"https://api.imgbun.com/jpg"

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

@bot.message_handler(regexp=CHORD_REGEX)
def send_chord_analysis(message):
    ch = pychord.Chord(message.text[1:-1])
    text = get_chord_analysis_message(ch)
    bot.reply_to(message, text, parse_mode="MARKDOWN")

@bot.message_handler(regexp=COMPOSE_REGEX)
def send_compose_analysis(message):
    notes = message.text[1:-1].upper().split()
    text = get_compose_analysis_message(notes)
    bot.reply_to(message, text, parse_mode="MARKDOWN")


# INLINE MODE

@bot.inline_handler(lambda query: re.search(CHORD_REGEX, query.query))
def send_inline_chord_analysis(query):
    logger.info("Chord inline query: " + query.query)
    try:
        ch = pychord.Chord(query.query[1:-1])
        text = get_chord_analysis_message(ch)

        url = requests.post(CHORD_URL, data={"chord": ch.chord, "instrument": "piano"}).text.split("src=")[1][1:-2]
        thumb_url = requests.get(THUMBNAIL_URL, params={"key": IMGBUN_API_KEY, "text": ch.chord, "size": 8}).json()["direct_link"]
        logger.info(thumb_url)
        logger.info(url)
        r = types.InlineQueryResultPhoto(id='1', thumb_url=thumb_url, photo_url=url, photo_height=2, photo_width=2,
                                        title=f"Analysis of {ch.chord} chord", caption=text, parse_mode="MARKDOWN", 
                                        description="Click to see the chord analysis.")
        bot.answer_inline_query(query.id, [r])
    except Exception as e:
        logger.exception(e)

@bot.inline_handler(lambda query: re.search(COMPOSE_REGEX, query.query))
def send_inline_compose_analysis(query):
    logger.info("Compose inline query: " + query.query)
    try:
        notes = query.query[1:-1].upper().split()
        text = get_compose_analysis_message(notes)
        r = types.InlineQueryResultArticle(id='1', title=f"Find chord(s) from {' '.join(notes)}", input_message_content=types.InputTextMessageContent(text, parse_mode="MARKDOWN"),
                                           description=f"Click to see the possible chords.")
        bot.answer_inline_query(query.id, [r])
    except Exception as e:
        logger.exception(e)



if __name__ == '__main__':
    bot.infinity_polling(skip_pending=True)
else:
    pass