from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters


# здесь должен быть ваш токен
TOKEN = '<TOKEN>'


def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher
echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

updater.start_polling()
updater.idle()