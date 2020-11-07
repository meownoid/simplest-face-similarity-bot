import io
import dlib
import logging
import numpy as np
import pickle

from operator import itemgetter
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
from PIL import Image

logging.basicConfig(level='DEBUG')

# here should be your token
TOKEN = '<TOKEN>'

face_detector = dlib.get_frontal_face_detector()
shape_predictor = dlib.shape_predictor('assets/shape_predictor_5_face_landmarks.dat')
face_recognition_model = dlib.face_recognition_model_v1('assets/dlib_face_recognition_resnet_model_v1.dat')

with open('assets/embeddings.pickle', 'rb') as f:
    star_embeddings = pickle.load(f)


def handle_photo(bot, update):
    message = update.message
    photo = message.photo[~0]

    with io.BytesIO() as fd:
        file_id = bot.get_file(photo.file_id)
        file_id.download(out=fd)
        fd.seek(0)

        image = Image.open(fd)
        image.load()
        image = np.asarray(image)

    face_detects = face_detector(image, 1)

    if not face_detects:
        bot.send_message(chat_id=update.message.chat_id, text='no faces')

    face = face_detects[0]
    landmarks = shape_predictor(image, face)
    embedding = face_recognition_model.compute_face_descriptor(image, landmarks)
    embedding = np.asarray(embedding)

    ds = []

    for name, emb in star_embeddings:
        distance = np.linalg.norm(embedding - emb)
        ds.append((name, distance))

    best_match, best_distance = min(ds, key=itemgetter(1))

    bot.send_message(
        chat_id=update.message.chat_id,
        text=f'your look exactly like *{best_match}*',
        parse_mode='Markdown'
    )


updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher
photo_handler = MessageHandler(Filters.photo, handle_photo)
dispatcher.add_handler(photo_handler)

updater.start_polling()
updater.idle()
