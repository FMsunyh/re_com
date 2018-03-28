"""
Copyright 2017-2018 Fizyr (https://fizyr.com)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import json
from pprint import pprint

from utils.label import names_to_labels
from ..preprocessing.generator import Generator
from ..utils.image import read_image_bgr

import os
import numpy as np
from six import raise_from
from PIL import Image

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

# voc_classes = {
#     'aeroplane'   : 0,
#     'bicycle'     : 1,
#     'bird'        : 2,
#     'boat'        : 3,
#     'bottle'      : 4,
#     'bus'         : 5,
#     'car'         : 6,
#     'cat'         : 7,
#     'chair'       : 8,
#     'cow'         : 9,
#     'diningtable' : 10,
#     'dog'         : 11,
#     'horse'       : 12,
#     'motorbike'   : 13,
#     'person'      : 14,
#     'pottedplant' : 15,
#     'sheep'       : 16,
#     'sofa'        : 17,
#     'train'       : 18,
#     'tvmonitor'   : 19
# }

# com_classes = {
# 'ala-alabg-hz-ywjx-116g': 0,
#  'asm-asmnc-pz-yw-500ml': 1,
#  'bl-blht-dz-yw-6.7g': 2,
#  'bs-bskl-gz-yw-330ml': 3,
#  'bskl-bskl-pz-yw-600ml': 4,
#  'fd-fd-gz-yw-330ml': 5,
#  'glg-glgblzbg-hz-mcxcw-45g': 6,
#  'htk-tls-dz-hd-288g': 7,
#  'hwd-hwdfbm-tz-hxw-75g': 8,
#  'hwd-hwdfbm-tz-wxnrfw-84g': 9,
#  'jb-jbjyz-dz-yw-95g': 10,
#  'jdb-jdb-pz-yw-500ml': 11,
#  'jdb-jdblc-gz-yw-310ml': 12,
#  'kkkl-jcnmwqs-pz-nmw-500ml': 13,
#  'kkkl-kkkl-gz-yw-330ml': 14,
#  'kkkl-kkkl-pz-yw-600ml': 15,
#  'ksf-ksfbg-dz-qxnmw-125g': 16,
#  'ksf-ksfltscnrm-tz-scnr-82.5g': 17,
#  'lfe-lfeyrbttgsq-hz-yrbtr-30g': 18,
#  'llm-llm-dz-nmcm-60g': 19,
#  'ls-lssp-dz-mgjdyw-70g': 20,
#  'lzs-rnbdwhbg-hz-nlw-145g': 21,
#  'md-md-pz-qn-600ml': 22,
#  'mdl-mdlbxgg-dz-bxg-80g': 23,
#  'mn-zgl-pz-cmw-250ml': 24,
#  'nfsq-nfsq-pz-yw-550ml': 25,
#  'nfsq-nfsqc-pz-xymlhc-500ml': 26,
#  'nfsq-nfsqc-pz-yzlc-500ml': 27,
#  'qc-qckf-pz-shnt-268ml': 28,
#  'tdyh-tdyhpgc-gz-pg-330ml': 29,
#  'ty-hzy-pz-gw-500ml': 30,
#  'ty-tyhsnrm-tz-nr-105g': 31,
#  'ty-tyxmtx-pz-lpqnhc-480ml': 32,
#  'wl-wldmj-dz-lw-106g': 33,
#  'wlj-wlj-gz-yw-310ml': 34,
#  'wlj-wljlc-dz-yw-250ml': 35,
#  'wlj-wljlc-hz-yw-250ml': 36,
#  'wlj-wljlc-pz-yw-500ml': 37,
#  'wq-wqaljm-dz-al-50g': 38,
#  'wq-wqaljm-dz-al-60g': 39,
#  'wt-wtnmc-gz-yw-310ml': 40,
#  'wtn-wtnywdn-hz-yw-250ml': 41,
#  'wwsp-wwxxs-dz-yw-60g': 42,
#  'wwsp-wznn-hz-yw-125ml': 43,
#  'xb-xb-gz-yw-330ml': 44,
#  'yb-yb-pz-yw-550ml': 45,
#  'yd-ydmtcqscm-pz-cmw-56g': 46,
#  'yj-pjfz-dz-sjw-100g': 47,
#  'yl-ylcnn-hz-yw-250ml': 48,
#  'yl-ylhzdhmbbz-gz-hm-280g': 49,
#  'ys-zzyspyz-gz-yw-245ml': 50,
#  'yy-yylght-gz-ht-240ml': 51
# }



# def write_class_mapping():
#     with open('class_mapping.json', 'w+') as f:
#         json.dump(labels_to_names, f, sort_keys=True)
#         print('save the classs mapping.')




com_classes = names_to_labels()
print(com_classes)
print("")
#
# com_classes = {
#     'hz':0,
#     'dz':1,
#     'gz':2,
#     'pz':3,
#     'tz':4
# }

def _findNode(parent, name, debug_name = None, parse = None):
    if debug_name is None:
        debug_name = name

    result = parent.find(name)
    if result is None:
        raise ValueError('missing element \'{}\''.format(debug_name))
    if parse is not None:
        try:
            return parse(result.text)
        except ValueError as e:
            raise_from(ValueError('illegal value for \'{}\': {}'.format(debug_name, e)), None)
    return result


class PascalVocGenerator(Generator):
    def __init__(
        self,
        data_dir,
        set_name,
        classes=com_classes,
        image_extension='.jpg',
        skip_truncated=False,
        skip_difficult=False,
        **kwargs
    ):
        self.data_dir             = data_dir
        self.set_name             = set_name
        self.classes              = classes
        self.image_names          = [l.strip().split(None, 1)[0] for l in open(os.path.join(data_dir, 'ImageSets', 'Main', set_name + '.txt')).readlines()]
        self.image_extension      = image_extension
        self.skip_truncated       = skip_truncated
        self.skip_difficult       = skip_difficult

        self.labels = {}
        for key, value in self.classes.items():
            self.labels[value] = key

        super(PascalVocGenerator, self).__init__(**kwargs)

    def size(self):
        return len(self.image_names)

    def num_classes(self):
        return len(self.classes)

    def name_to_label(self, name):
        return self.classes[name]

    def label_to_name(self, label):
        return self.labels[label]

    def image_aspect_ratio(self, image_index):
        path  = os.path.join(self.data_dir, 'JPEGImages', self.image_names[image_index] + self.image_extension)
        try:
            image = Image.open(path)
        except Exception as ex:
            print(ex)

        return float(image.width) / float(image.height)

    def load_image(self, image_index):
        path = os.path.join(self.data_dir, 'JPEGImages', self.image_names[image_index] + self.image_extension)
        return read_image_bgr(path)

    def __parse_annotation(self, element):
        truncated = _findNode(element, 'truncated', parse=int)
        difficult = _findNode(element, 'difficult', parse=int)

        class_name = _findNode(element, 'name').text
        if class_name not in self.classes:
            raise ValueError('class name \'{}\' not found in classes: {}'.format(class_name, list(self.classes.keys())))

        box = np.zeros((1, 5))
        box[0, 4] = self.name_to_label(class_name)

        bndbox    = _findNode(element, 'bndbox')
        box[0, 0] = _findNode(bndbox, 'xmin', 'bndbox.xmin', parse=float) - 1
        box[0, 1] = _findNode(bndbox, 'ymin', 'bndbox.ymin', parse=float) - 1
        box[0, 2] = _findNode(bndbox, 'xmax', 'bndbox.xmax', parse=float) - 1
        box[0, 3] = _findNode(bndbox, 'ymax', 'bndbox.ymax', parse=float) - 1

        return truncated, difficult, box

    # def __parse_annotation(self, element):
    #     truncated = _findNode(element, 'truncated', parse=int)
    #     difficult = _findNode(element, 'difficult', parse=int)
    #
    #     class_name = _findNode(element, 'name').text
    #     class_name = class_name.split('-')[2]
    #     if class_name not in self.classes:
    #         raise ValueError('class name \'{}\' not found in classes: {}'.format(class_name, list(self.classes.keys())))
    #
    #     box = np.zeros((1, 5))
    #     box[0, 4] = self.name_to_label(class_name)
    #
    #     bndbox    = _findNode(element, 'bndbox')
    #     box[0, 0] = _findNode(bndbox, 'xmin', 'bndbox.xmin', parse=float) - 1
    #     box[0, 1] = _findNode(bndbox, 'ymin', 'bndbox.ymin', parse=float) - 1
    #     box[0, 2] = _findNode(bndbox, 'xmax', 'bndbox.xmax', parse=float) - 1
    #     box[0, 3] = _findNode(bndbox, 'ymax', 'bndbox.ymax', parse=float) - 1
    #
    #     return truncated, difficult, box

    def __parse_annotations(self, xml_root):
        size_node = _findNode(xml_root, 'size')
        width     = _findNode(size_node, 'width',  'size.width',  parse=float)
        height    = _findNode(size_node, 'height', 'size.height', parse=float)

        boxes = np.zeros((0, 5))
        for i, element in enumerate(xml_root.iter('object')):
            try:
                truncated, difficult, box = self.__parse_annotation(element)
            except ValueError as e:
                raise_from(ValueError('could not parse object #{}: {}'.format(i, e)), None)

            if truncated and self.skip_truncated:
                continue
            if difficult and self.skip_difficult:
                continue
            boxes = np.append(boxes, box, axis=0)

        return boxes

    def load_annotations(self, image_index):
        filename = self.image_names[image_index] + '.xml'
        try:
            tree = ET.parse(os.path.join(self.data_dir, 'Annotations', filename))
            return self.__parse_annotations(tree.getroot())
        except ET.ParseError as e:
            raise_from(ValueError('invalid annotations file: {}: {}'.format(filename, e)), None)
        except ValueError as e:
            raise_from(ValueError('invalid annotations file: {}: {}'.format(filename, e)), None)
