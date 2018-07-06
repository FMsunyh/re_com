#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 3/26/2018 11:56 AM 
# @Author : sunyonghai 
# @File : test.py 
# @Software: ZJ_AI
# =========================================================
import argparse
import json
import os
from pprint import pprint

import cv2
import tensorflow as tf
import keras
import time
import numpy as np
from PIL import Image

from keras_retinanet.utils.label import labels_to_names

from keras_retinanet.models.resnet import custom_objects
from keras_retinanet.utils.colors import label_color
from keras_retinanet.utils.image import read_image_bgr, preprocess_image, resize_image
from data_processing.io_utils import *
from keras_retinanet.utils.visualization import draw_box, draw_caption
from lxml.etree import Element, SubElement, tostring
from xml.dom.minidom import parseString


from config import MODEL_PATH, ROOT_HOME

parser = argparse.ArgumentParser(description='Get the data info')
parser.add_argument('-d', '--data_dir',help='predect data', default='')
parser.add_argument('-m', '--model_file',help='model path', default='')
args = parser.parse_args()

# DATA_DIR = 'data/train_data-2018-04-12'
DATA_DIR = args.data_dir
MODEL_PATH = args.model_file

# DATA_DIR = 'data/train_data-2018-04-09-2'
# DATA_DIR = 'data/train_data-2018-03-30'
# TEST_DATA_DIR = os.path.join(ROOT_HOME, DATA_DIR, 'JPEGImages/')
# TEST_RESULT_DIR = os.path.join(ROOT_HOME,DATA_DIR, 'JPEGImages_bbox/')
# TEST_ANNOTATION_DIR = os.path.join(ROOT_HOME,DATA_DIR, 'Annotations/')

TEST_DATA_DIR = os.path.join( DATA_DIR, 'JPEGImages/')
TEST_RESULT_DIR = os.path.join(DATA_DIR, 'JPEGImages_bbox/')
TEST_ANNOTATION_DIR = os.path.join(DATA_DIR, 'Annotations/')

threshold = 0.7

Debug = True
def get_session():
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    return tf.Session(config=config)

keras.backend.tensorflow_backend.set_session(get_session())

model = keras.models.load_model(MODEL_PATH, custom_objects=custom_objects)

# load label to names mapping for visualization purposes
labels_to_names = labels_to_names()

class ImageInfo(object):
    def __init__(self, name='', path='', image_extension='.jpg', image_bgr=None):
        self.name = name # not include extension
        self.path = path
        self.image_extension = image_extension
        self.image_bgr = image_bgr
        self.width=0
        self.height=0
        self.channel=3

def get_images(image_dir):
    if image_dir == '':
        return []

    images =[]

    paths = [os.path.join(image_dir, s) for s in os.listdir(image_dir)]
    for path in paths:
       im = read_image_bgr(path)
       images.append(im)

    return images


def get_imageinfos(image_dir):
    if image_dir == '':
        return []

    imageinfos =[]

    for s in os.listdir(image_dir):
        name = s.split('.')[0]
        extension = s.split('.')[1]
        path = os.path.join(image_dir, s)
        # im = read_image_bgr(path)
        im = path
        im_info = ImageInfo(name=name, path=path, image_extension=extension, image_bgr=im)
        imageinfos.append(im_info)

    print('Read the images.Finished!')
    return imageinfos


def save_image(image, path):
    im = Image.fromarray(image)
    im.save(path)
    print('save the image to {}'.format(path))


def predict_imageinfo(imageinfos):

    if len(imageinfos)<=0:
        return

    print('start predict.....................')
    for item in imageinfos:
        # image = item.image_bgr
        image = read_image_bgr(item.path)
        item.width = image.shape[1]
        item.height = image.shape[0]
        item.channel = image.shape[2]
        predicted_labels, scores, detections = predict(image)
        # draw = image.copy()
        # draw = cv2.cvtColor(draw, cv2.COLOR_BGR2RGB)
        # image_draw = visualize(draw, predicted_labels, scores, detections)

        # save_path = os.path.join(TEST_RESULT_DIR, item.name + '.' + item.image_extension)
        # save_image(image_draw, save_path)
        save_annotations(TEST_ANNOTATION_DIR, item, predicted_labels, scores, detections)

def predict(image):
    image = preprocess_image(image)
    image, scale = resize_image(image)

    # process image
    start = time.time()
    a, b, detections = model.predict_on_batch(np.expand_dims(image, axis=0))
    print("processing time: ", str(1000 * (time.time() - start)) + " ms")

    # compute predicted labels and scores
    predicted_labels = np.argmax(detections[0, :, 4:], axis=1)
    scores = detections[0, np.arange(detections.shape[1]), 4 + predicted_labels]

    # correct for image scale
    detections[0, :, :4] /= scale

    return predicted_labels, scores, detections


def visualize(draw, predicted_labels, scores, detections):
    for idx, (label, score) in enumerate(zip(predicted_labels, scores)):
        if score < 0.7:
            continue

        color = label_color(label)

        b = detections[0, idx, :4].astype(int)
        draw_box(draw, b, color=color)

        caption = "{} {:.3f}".format(labels_to_names[label], score)
        draw_caption(draw, b, caption)

    return draw


def check_border(bbox, width, height):
    if len(bbox) <4:
        return

    if bbox[0] <= 0.0:
        bbox[0]= 1

    if bbox[1] <= 0.0:
        bbox[1] = 1

    if bbox[2] >= width:
        bbox[2] = width - 1

    if bbox[3] >= height:
        bbox[3] = height - 1

def make_xml(im_info, predicted_labels, scores, detections):
    node_root = Element('annotation')
    node_folder = SubElement(node_root, 'folder')
    node_folder.text = 'JPEGImages'
    node_filename = SubElement(node_root, 'filename')
    node_filename.text = im_info.name + '.' +im_info.image_extension

    node_path = SubElement(node_root, 'path')
    node_path.text = im_info.path

    node_size = SubElement(node_root, 'size')
    node_width = SubElement(node_size, 'width')
    node_width.text =str(im_info.width)

    node_height = SubElement(node_size, 'height')
    node_height.text =str(im_info.height)

    node_depth = SubElement(node_size, 'depth')
    node_depth.text = str(im_info.channel)

    node_segmented = SubElement(node_root, 'segmented')
    node_segmented.text = '0'

    for idx, (label, score) in enumerate(zip(predicted_labels, scores)):
        if score < 0.7:
            continue

        node_object = SubElement(node_root, 'object')
        node_name = SubElement(node_object, 'name')
        caption = "{}".format(labels_to_names[label])
        node_name.text = caption

        node_pose = SubElement(node_object, 'pose')
        node_pose.text = 'Unspecified'

        node_truncated = SubElement(node_object, 'truncated')
        node_truncated.text = '0'

        node_difficult = SubElement(node_object, 'difficult')
        node_difficult.text = '0'

        b = detections[0, idx, :4].astype(int)
        check_border(b, im_info.width,im_info.height)

        node_bndbox = SubElement(node_object, 'bndbox')
        node_xmin = SubElement(node_bndbox, 'xmin')
        node_xmin.text = str(int(b[0]))

        node_ymin = SubElement(node_bndbox, 'ymin')
        node_ymin.text = str(int(b[1]))

        node_xmax = SubElement(node_bndbox, 'xmax')
        node_xmax.text = str(int(b[2]))

        node_ymax = SubElement(node_bndbox, 'ymax')
        node_ymax.text = str(int(b[3]))

    xml = tostring(node_root, pretty_print=True)
    dom = parseString(xml)
    # print xml 打印查看结果

    return dom


def _beautifulFormat(xmlDomObject):
    '''美化xml格式
    '''
    if xmlDomObject:
        # 优化格式显示
        xmlStr = xmlDomObject.toprettyxml(indent='', newl='', encoding='utf-8')
        xmlStr = xmlStr.replace(b'\t', b'').replace(b'\n', b'')
        xmlDomObject = parseString(xmlStr)
        xmlStr = xmlDomObject.toprettyxml(indent='\t', newl='\n', encoding='utf-8')
        dom = parseString(xmlStr)
        return dom
    else:
        return False

def save_annotations(save_dir, im_info,predicted_labels, scores, detections):
    dom = make_xml(im_info,predicted_labels, scores, detections)
    # dom = _beautifulFormat(dom)
    # mkdir(save_dir)
    xml_path = os.path.join(save_dir, im_info.name + '.xml')
    with open(xml_path, 'w+') as f:
        dom.writexml(f, addindent='', newl='', encoding='utf-8')

    # return True

if __name__ == '__main__':
    imageinfos = get_imageinfos(TEST_DATA_DIR)

    mkdir(TEST_ANNOTATION_DIR)
    mkdir(TEST_RESULT_DIR)

    remove_all(TEST_ANNOTATION_DIR)
    remove_all(TEST_RESULT_DIR)

    predict_imageinfo(imageinfos)

"""
cd /home/syh/RetinaNet/data_processing
python /home/syh/RetinaNet/keras_retinanet/bin/test.py -d /home/syh/RetinaNet/data_52/test -m /home/syh/RetinaNet/snapshots/resnet101_pascal_3_02.h5
"""