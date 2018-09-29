# -----------------------------------------------------
# -*- coding: utf-8 -*-
# @Time    : 8/29/2018 6:13 PM
# @Author  : sunyonghai
# @Software: ZJ_AI
# -----------------------------------------------------
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

import shutil

from data_processing.fusion_voc.fusion_utils import *

voc_home = '/home/syh/tf-faster-rcnn/data/VOCdevkit2012/VOC2012'
JPEGImages_path = os.path.join(voc_home, 'JPEGImages')
Annotations_path = os.path.join(voc_home, 'Annotations')
SegmentationObject_path = os.path.join(voc_home, 'SegmentationObject')

output = '/home/syh/tf-faster-rcnn/data/fusion/output/VOC2012'

root_home = '/home/syh/tf-faster-rcnn/data/fusion/'
bg_path = os.path.join(root_home, 'bg/background_min_800/')

def process(name):
    # read SegmentationObject
    seg_path = os.path.join(SegmentationObject_path, name+'.png')
    seg_png = load_image(seg_path)
    # print(seg_png[:,:,0])
    # print(seg_png[:,:,1])
    # print(seg_png[:,:,2])

    # read JPEGImages
    jpeg_path = os.path.join(JPEGImages_path, name+'.jpg')
    jpeg = load_image(jpeg_path)

    png = create_png(seg_png, jpeg)

    out_path = os.path.join(output,'png', name+'.png')
    save_image(out_path, png)

    # read BG
    bg_path = next(gen_bg)
    bg = load_image(bg_path)
    re_bg = resize_image(np.transpose(bg,[1,0,2]), (jpeg.shape[1],jpeg.shape[0]))

    result = composite_bg(re_bg, png)

    jpg_path = os.path.join(output,'JPEGImages', name+'.jpg')
    save_image(jpg_path, result)

    anno_dir = os.path.join(output,'Annotations')
    if not os.path.exists(anno_dir):
        os.makedirs(anno_dir)

    srcfile = os.path.join(Annotations_path, name+'.xml')
    dstfile = os.path.join(anno_dir, name+'.xml')
    shutil.copyfile(srcfile,dstfile)

if __name__ == '__main__':
    gen_bg = load_segmentation_object(bg_path)

    names = os.listdir(SegmentationObject_path)
    for file_name in names:
        filename, extension = os.path.splitext(file_name)
        process(filename)
        print(filename)