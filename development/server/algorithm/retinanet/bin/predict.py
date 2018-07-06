#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 3/26/2018 11:56 AM 
# @Author : sunyonghai 
# @File : predict.py
# @Software: ZJ_AI
# =========================================================

import keras
import numpy as np

from server.algorithm.retinanet import models
from server.algorithm.retinanet.config import MODEL_PATH
from server.algorithm.retinanet.utils.colors import label_color
from server.algorithm.retinanet.utils.image import read_image_bgr, preprocess_image, resize_image
from server.algorithm.retinanet.utils.label import *
from server.algorithm.retinanet.utils.visualization import draw_box, draw_caption
from server.algorithm.utils import *

def get_session():
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    return tf.Session(config=config)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
keras.backend.tensorflow_backend.set_session(get_session())

# load label to names mapping for visualization purposes
labels_to_names = labels_to_names()

def load_model(load=False):
    if load:
        try:
            print('loading the model...............')
            model = models.load_model(MODEL_PATH, backbone_name='resnet50',convert=True)
            image_path = '/home/syh/commdity_recognition/development/server/data/download/train_20180307_1725.jpg'
            image = read_image_bgr(image_path)
            image = preprocess_image(image)
            image, scale = resize_image(image)
            model.predict_on_batch(np.expand_dims(image, axis=0))
            print('finished load the model...............')

            # print(model.summary())
        except ImportError as ex:
            print("Can't load the model: %s" % ex)
    else:
        return None

    return model

# predict_model = load_model()
predict_model = load_model()

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
    global predict_model
    if predict_model is None:
        predict_model = load_model()

    image = preprocess_image(image)
    image, scale = resize_image(image)

    # print(predict_model.summary())
    # process image
    start = time.time()
    boxes, scores, labels = predict_model.predict_on_batch(np.expand_dims(image, axis=0))
    print("processing time: ", str(1000 * (time.time() - start)) + " ms")

    # # correct for image scale
    boxes/= scale

    return boxes, scores, labels


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

# def get_prediect_label_bbox(boxes, scores, labels):
#     data = []
#     for box, score, label in zip(boxes[0], scores[0], labels[0]):
#         # scores are sorted so we can break
#         if score < threshold:
#             break
#
#         caption = "{}".format(labels_to_names[label])
#         score = "{:.3f}".format(score)
#         box =box.astype(int)
#         data.append("{},{},{},{},{},{}".format(caption, score, box[0], box[1],box[2], box[3] ))
#     return data


def get_prediect_label_bbox(predicted_labels, scores, detections):
    data = ["{},{:.3f},{},{},{},{}".format('glg-glgblzbg-hz-mcxcw-45g',0.931,1049,570,1492,1103)]
    data.append("{},{:.3f},{},{},{},{}".format('bl-blht-dz-yw-6.7g',0.850,493,516,1121,1148))
    data.append("{},{:.3f},{},{},{},{}".format('bl-blht-dz-yw-6.7g',0.850,493,516,1121,1148))
    data.append("{},{:.3f},{},{},{},{}".format('wwsp-wwxxs-dz-yw-60g',0.838,660,253,1248,591))
    data.append("{},{:.3f},{},{},{},{}".format('wwsp-wwxxs-dz-yw-60g',0.838,660,253,1248,591))
    data.append("{},{:.3f},{},{},{},{}".format('wwsp-wwxxs-dz-yw-60g',0.838,660,253,1248,591))
    return data

# def get_class_count(predicted_labels, scores):
#     classes_count = {}
#     for idx, (label, score) in enumerate(zip(predicted_labels, scores)):
#         if score < threshold:
#             continue
#
#         class_name = labels_to_names[label]
#         if class_name not in classes_count:
#             classes_count[class_name] = 1
#         else:
#             classes_count[class_name] += 1
#
#     return classes_count
#
# def save_annotations(save_dir, predicted_labels, scores, detections):
#     pass

if __name__ == '__main__':
    image_path = '/home/syh/commdity_recognition/development/server/data/download/train_20180307_1725.jpg'

    image = read_image_bgr(image_path)
    boxes, scores, labels = predict(image)
