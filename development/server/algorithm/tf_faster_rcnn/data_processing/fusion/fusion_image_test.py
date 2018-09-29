# -----------------------------------------------------
# -*- coding: utf-8 -*-
# @Time    : 8/23/2018 10:15 AM
# @Author  : sunyonghai
# @Software: ZJ_AI
# -----------------------------------------------------
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import pytest
from PIL import Image
import numpy as np
import os
import tempfile
import shutil
import cv2
from data_processing.fusion.fusion_image import *

import data_processing.fusion.fusion_


class TestImage(object):

    def setup_class(cls):
        cls.root_path = '...../tf-faster-rcnn/data/fusion/'

    def teardown_class(cls):
        pass

    def test_create_png(self):
        obj_mask_path = os.path.join(self.root_path, 'obj_165_mask/aebs-aebsntbbt-dz-hhkw-120g/0.png')
        origin_obj_path = os.path.join(self.root_path, 'obj_165/aebs-aebsntbbt-dz-hhkw-120g/0.jpg')
        output_path = os.path.join(self.root_path, 'obj_165_png/aebs-aebsntbbt-dz-hhkw-120g/0.png')

        obj_mask_img = cv2.imread(obj_mask_path)
        origin_obj_img = cv2.imread(origin_obj_path)

        res = create_png(obj_mask_img, origin_obj_img, output_path)
        assert res is not None

    def test_composite_data(self):
        bg_path = os.path.join(self.root_path,'bg/bg_2018-05-30_10466.jpg')
        obj_png_path = os.path.join(self.root_path, 'obj_165_png/aebs-aebsntbbt-dz-hhkw-120g/0.png')
        bg = cv2.imread(bg_path)
        obj_png =cv2.imread(obj_png_path, cv2.IMREAD_UNCHANGED)

        output_path = os.path.join(root_path, 'output/JPEGImages/composite.jpg')
        composite_data(bg, obj_png, output_path)

    def test_find_bbox(self):
        obj_mask_path = os.path.join(self.root_path, 'obj_165_mask/aebs-aebsntbbt-dz-hhkw-120g/0.png')
        obj_mask_img = cv2.imread(obj_mask_path)

        bboxes = find_bbox(obj_mask_img)
        print(bboxes)
        assert len(bboxes) > 0

    def test_paste_obj(self):
        path = os.path.join(self.root_path, "mask/aebs-aebsntbbt-dz-hhkw-120g/0.png")

        obj_png = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        output_path = os.path.join(root_path, 'output/JPEGImages/paste_obj.png')

        img = paste_obj(obj_png,(3600,3600))
        save_image(output_path, img)

    if __name__ == '__main__':
        pytest.main([__file__])
        # pytest.main()