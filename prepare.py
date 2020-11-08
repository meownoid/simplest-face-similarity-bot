import os
import pickle
import sys
import urllib.request

import dlib
import numpy as np
from PIL import Image

import config

if not os.path.exists(config.LANDMARKS_PATH) and config.DOWNLOAD_ASSETS:
    print('Downloading landmarks model')
    os.makedirs(os.path.dirname(config.LANDMARKS_PATH), exist_ok=True)
    urllib.request.urlretrieve(config.LANDMARKS_URL, config.LANDMARKS_PATH)

if not os.path.exists(config.MODEL_PATH) and config.DOWNLOAD_ASSETS:
    print('Downloading face model')
    os.makedirs(os.path.dirname(config.MODEL_PATH), exist_ok=True)
    urllib.request.urlretrieve(config.MODEL_URL, config.MODEL_PATH)

face_detector = dlib.get_frontal_face_detector()
shape_predictor = dlib.shape_predictor(config.LANDMARKS_PATH)
face_recognition_model = dlib.face_recognition_model_v1(config.MODEL_PATH)

fs = os.listdir(config.PHOTOS_DIR)

if not fs:
    print(f'{config.PHOTOS_DIR} is empty')
    sys.exit(1)

es = []

for f in fs:
    print(f'Processing {f}')

    image = np.asarray(Image.open(os.path.join(config.PHOTOS_DIR, f)))
    face_detects = face_detector(image, 1)
    face = face_detects[0]
    landmarks = shape_predictor(image, face)
    embedding = face_recognition_model.compute_face_descriptor(image, landmarks, num_jitters=10)
    embedding = np.asarray(embedding)

    name, _ = os.path.splitext(f)
    es.append((name, embedding))

with open(os.path.join(config.ASSETS_DIR, 'embeddings.pickle'), 'wb') as f:
    pickle.dump(es, f)
