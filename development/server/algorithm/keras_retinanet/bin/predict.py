#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 3/26/2018 11:56 AM 
# @Author : sunyonghai 
# @File : predict.py
# @Software: ZJ_AI
# =========================================================
import json
import os
from pprint import pprint

import tensorflow as tf
import keras
import time
import numpy as np
from PIL import Image

from server.algorithm.keras_retinanet.config import MODEL_PATH
from server.algorithm.keras_retinanet.models.resnet import custom_objects
from server.algorithm.keras_retinanet.utils.colors import label_color
from server.algorithm.keras_retinanet.utils.image import read_image_bgr, preprocess_image, resize_image
from server.algorithm.keras_retinanet.utils.io_utils import *
from server.algorithm.keras_retinanet.utils.visualization import draw_box, draw_caption
from server.algorithm.utils import *

from server.algorithm.keras_retinanet.utils.label import *

Debug = True
def get_session():
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    return tf.Session(config=config)

# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
# os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
# os.environ["CUDA_VISIBLE_DEVICES"] = ""
# keras.backend.tensorflow_backend.set_session(get_session())


# load label to names mapping for visualization purposes
labels_to_names = labels_to_names()

global model

def load_model():
    global model

    try:
        print('loading the model...............')
        model = keras.models.load_model(MODEL_PATH, custom_objects=custom_objects)
        # model = load_model(FLAGS.xception_model)
    except ImportError as ex:
        print("Can't load the model: %s" % ex)

    return model

def get_images(image_dir):
    if image_dir == '':
        return []

    images =[]

    paths = [os.path.join(image_dir, s) for s in os.listdir(image_dir)]
    for path in paths:
       im = read_image_bgr(path)
       images.append(im)

    return images


def predict(image):

    global model
    if model is None:
        model = load_model()

    image = preprocess_image(image)
    image, scale = resize_image(image)

    # process image
    start = time.time()
    _, _, detections = model.predict_on_batch(np.expand_dims(image, axis=0))
    print("processing time: ", str(1000 * (time.time() - start)) + " ms")

    # compute predicted labels and scores
    predicted_labels = np.argmax(detections[0, :, 4:], axis=1)
    scores = detections[0, np.arange(detections.shape[1]), 4 + predicted_labels]

    # correct for image scale
    detections[0, :, :4] /= scale

    return predicted_labels, scores, detections

threshold = 0.7
def visualize(draw, predicted_labels, scores, detections):
    for idx, (label, score) in enumerate(zip(predicted_labels, scores)):
        if score < threshold:
            continue

        color = label_color(label)

        b = detections[0, idx, :4].astype(int)
        draw_box(draw, b, color=color)

        caption = "{} {:.3f}".format(labels_to_names[label], score)
        draw_caption(draw, b, caption)

    return draw
    # im = Image.fromarray(draw)
    # im.save("1072.jpg")

def get_class_count(predicted_labels, scores):
    classes_count = {}
    for idx, (label, score) in enumerate(zip(predicted_labels, scores)):
        if score < threshold:
            continue

        class_name = labels_to_names[label]
        if class_name not in classes_count:
            classes_count[class_name] = 1
        else:
            classes_count[class_name] += 1

    return classes_count

def save_annotations(save_dir, predicted_labels, scores, detections):
    pass

# image = read_image_bgr(os.path.join(test_data_dir, '000000008021.jpg'))
# print(image)