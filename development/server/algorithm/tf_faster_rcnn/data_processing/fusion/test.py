# -----------------------------------------------------
# -*- coding: utf-8 -*-
# @Time    : 8/23/2018 9:11 AM
# @Author  : sunyonghai
# @Software: ZJ_AI
# -----------------------------------------------------
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import itertools
import data_processing.fusion.fusion_utils
import data_processing.fusion.generator
import data_processing.fusion.iou_utils

if __name__ == '__main__':
    s = [1, 2, 3, 4]
    gen = itertools.cycle(s)

    for _ in range(3):
        print(gen.__next__())