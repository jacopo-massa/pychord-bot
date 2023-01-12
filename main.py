import telebot
import pychord
import os
import re
import logging
import requests
import flask

from telebot import types
from messages import *
from analysis import *


# get environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
IMGBUN_API_KEY = os.getenv('IMGBUN_API_KEY')

CHORD_REGEX = "\[\S+\]"
COMPOSE_REGEX = "\{([A-Z#b]|\s)+\}"

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="MARKDOWN")
logger = telebot.logger
telebot.logger.setLevel(logging.INFO) # Outputs debug messages to console.

app = flask.Flask(__name__)

# Empty webserver index, return nothing, just http 200
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return ''

# Process webhook calls
@app.route('/handle-messages', methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        app.logger.debug(f"JSON: {json_string}")
        update = types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    else:
        flask.abort(403)


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
    try:
        ch = pychord.Chord(message.text[1:-1])
        text = get_chord_analysis_message(ch)
        url = get_chord_image_url(ch)
        bot.send_photo(message.chat.id, url, caption=text, parse_mode="MARKDOWN", reply_to_message_id=message.message_id)
    except Exception as e:
        logger.exception(e)
        bot.reply_to(message, f"*{str(e)}*", parse_mode="MARKDOWN")

@bot.message_handler(regexp=COMPOSE_REGEX)
def send_compose_analysis(message):
    try:
        notes = message.text[1:-1].upper().split()
        text = get_compose_analysis_message(notes)
        bot.reply_to(message, text, parse_mode="MARKDOWN")
    except Exception as e:
        logger.exception(e)
        bot.reply_to(message, f"*{str(e)}*", parse_mode="MARKDOWN")


# INLINE MODE

@bot.inline_handler(lambda query: re.search(CHORD_REGEX, query.query))
def send_inline_chord_analysis(query):
    try:
        ch = pychord.Chord(query.query[1:-1])
        text = get_chord_analysis_message(ch)
        url = get_chord_image_url(ch)
        r = types.InlineQueryResultPhoto(id='1', thumb_url=url, photo_url=url, photo_height=1800, photo_width=2880,
                                        title=f"Analysis of {ch.chord} chord", caption=text, parse_mode="MARKDOWN", 
                                        description="Click to see the chord analysis.")
        bot.answer_inline_query(query.id, [r])
    except Exception as e:
        logger.exception(e)

@bot.inline_handler(lambda query: re.search(COMPOSE_REGEX, query.query))
def send_inline_compose_analysis(query):
    try:
        notes = query.query[1:-1].upper().split()
        text = get_compose_analysis_message(notes)
        r = types.InlineQueryResultArticle(id='1', title=f"Find chord(s) from {' '.join(notes)}",
                                        input_message_content=types.InputTextMessageContent(text, parse_mode="MARKDOWN"),
                                        description=f"Click to see the possible chords.")
        bot.answer_inline_query(query.id, [r])
    except Exception as e:
        logger.exception(e)


if __name__ == '__main__':
    # bot.remove_webhook()
    bot.infinity_polling(skip_pending=True)
else:
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

    telebot.logger.handlers = gunicorn_logger.handlers
    telebot.logger.setLevel(gunicorn_logger.level)