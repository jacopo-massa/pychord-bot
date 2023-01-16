from pychordbot import bot, app

import os
import logging
import telebot

# get desired webhook url, if set
WEBHOOK_URL = os.getenv('WEBHOOK_URL')


# reset webhook, if set
bot.reset_webhook()

# if running locally, start polling, else set desired webhook
if __name__ == '__main__':
    bot.infinity_polling(skip_pending=True)
else:
    bot.set_webhook(url=WEBHOOK_URL)

    # flask app and bot logger handlers are redirect to gunicorn web server ones, 
    # which is (preferably) used to run the bot on the major hosting platforms

    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

    telebot.logger.handlers = gunicorn_logger.handlers
    telebot.logger.setLevel(gunicorn_logger.level)