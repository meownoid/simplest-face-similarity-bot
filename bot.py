from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters


# здесь должен быть ваш токен
TOKEN = '<TOKEN>'


def handle_photo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='nice')


updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher
photo_handler = MessageHandler(Filters.photo, handle_photo)
dispatcher.add_handler(photo_handler)

updater.start_polling()
updater.idle()