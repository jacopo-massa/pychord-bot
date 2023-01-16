from pychordbot import bot, app

import os
import logging

# get desired webhook, if set
WEBHOOK_URL = os.getenv('WEBHOOK_URL')


# if running locally, reset webhook and start polling, else set desired webhook
if __name__ == '__main__':
    bot.remove_webhook()
    bot.infinity_polling(skip_pending=True)
else:
    bot.remove_webhook() # reset webhook
    bot.set_webhook(url=WEBHOOK_URL)

    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

    telebot.logger.handlers = gunicorn_logger.handlers
    telebot.logger.setLevel(gunicorn_logger.level)