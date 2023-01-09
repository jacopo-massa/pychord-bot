import telebot
import pychord

# get bot token as environment variable
BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)


if __name__ == '__main__':
    bot.infinity_polling(skip_pending=True)
else:
    pass