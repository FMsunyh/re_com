#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 3/28/2018 8:55 AM 
# @Author : sunyonghai 
# @File : label.py 
# @Software: ZJ_AI
# =========================================================
import json


mapping_path = '/home/syh/commdity_recognition/development/server/algorithm/keras_retinanet/name_to_label.json'

def _write_class_mapping(path):
    with open(path, 'w+') as f:
        json.dump(labels_to_names, f, sort_keys=True)
        print('save the classs mapping.')

def _read_class_mapping(path):
    with open(path, 'r') as f:
        # names_to_labels
        data = json.load(f)
        # pprint('mapping info:', labels_to_names)
    return data

def names_to_labels():
    result = _read_class_mapping(mapping_path)
    return result

def labels_to_names():
    labels_to_names = _read_class_mapping(mapping_path)
    result = {value:key for key, value in labels_to_names.items()}
    return result