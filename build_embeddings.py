import os
import dlib
import numpy as np
import pickle
from PIL import Image

face_detector = dlib.get_frontal_face_detector()
shape_predictor = dlib.shape_predictor('assets/shape_predictor_5_face_landmarks.dat')
face_recognition_model = dlib.face_recognition_model_v1('assets/dlib_face_recognition_resnet_model_v1.dat')

fs = os.listdir('photos')
es = []

for f in fs:
    print(f)

    image = np.asarray(Image.open(os.path.join('photos', f)))
    face_detects = face_detector(image, 1)
    face = face_detects[0]
    landmarks = shape_predictor(image, face)
    embedding = face_recognition_model.compute_face_descriptor(image, landmarks, num_jitters=10)
    embedding = np.asarray(embedding)

    name, _ = os.path.splitext(f)
    es.append((name, embedding))

with open('assets/embeddings.pickle', 'wb') as f:
    pickle.dump(es, f)
