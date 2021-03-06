# -----------------------------------------------------
# -*- coding: utf-8 -*-
# @Time    : 8/9/2018 4:34 PM
# @Author  : sunyonghai
# @Software: ZJ_AI
# -----------------------------------------------------
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tools import _init_paths
from model.config import cfg

import cv2
import argparse
import os.path as osp
import numpy as np

from lib.datasets import pascal_voc

from morelib.utils import cal_acc
from morelib.utils.prepare_model import *
from morelib.utils.xml_store import *
from tools.evaluate_net import predict_images

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='Tensorflow Faster R-CNN demo')
    parser.add_argument('--net', dest='demo_net', help='Network to use [vgg16 res101]',
                        default='vgg16')
    parser.add_argument('--dataset', dest='dataset', help='Trained dataset [pascal_voc pascal_voc_0712]',
                        default='pascal_voc_0712')
    parser.add_argument('--root_dir', dest='root_dir', help='the path of the file hava stored',
                         default=osp.join(cfg.ROOT_DIR,"data"))
    parser.add_argument('--model_dir', dest='model_dir', help='the path of  stored the model file',
                        default=osp.join(cfg.ROOT_DIR, "data","model"))
    parser.add_argument('--model_data', dest='model_data', help='the name of  stored the model file',
                        default="vgg16_2018-08-28-09_iter_110000.ckpt")
    parser.add_argument('--predict_dir', dest='predict_dir', help='prepare to predict this image',
                        default=osp.join(cfg.ROOT_DIR, "data","predict_data"))
    parser.add_argument('--package_data', dest='package_data', help='the test data file name',
                        default=["random_choice_data_3000"],type=list)
    parser.add_argument('--com_classes', dest='com_classes',
                        help='use com_classes file name',
                        default='com_classes_166.txt', type=str)
    args = parser.parse_args()

    return args



args = parse_args()
CLASSES = pascal_voc.read_classes(os.path.join(cfg.ROOT_DIR,'experiments', 'classes_cfgs',args.com_classes))

def main():
    cfg.TEST.HAS_RPN = True  # Use RPN for proposals

    tf_model = get_tf_model(args.model_dir, args.model_data)
    # set config
    tfconfig = tf.ConfigProto(allow_soft_placement=True)
    tfconfig.gpu_options.allow_growth = True

    # init session
    sess = tf.Session(config=tfconfig)
    # load network
    saver, net = load_model(sess, args.demo_net, tf_model, len(CLASSES))
    test_infos=[]
    for i,package in enumerate(args.package_data):
        jpg_files, xml_path = load_forecast_files(os.path.join(args.predict_dir, package))
        aps=predict_images(sess, net, jpg_files, xml_path,CLASSES)
        true_xml_path=os.path.join(args.predict_dir,package,'Annotations')
        test_xml_path = os.path.join(args.predict_dir, package, 'Annotations_test')
        test_info=cal_acc.cal_model_acc(test_xml_path,true_xml_path)
        test_info_label=cal_acc.cal_label_acc(test_xml_path,true_xml_path,CLASSES)
        print(test_info_label)
        for index in np.argsort(aps):
            test_infos.append("{},{},{},{},{}".format(args.model_data.split(".")[0],package,CLASSES[index+1],test_info_label[index+1],round(aps[index],6)))
        test_infos.append("{},{},total,{},{}".format(args.model_data.split(".")[0],package,test_info,round(np.nanmean(aps),6)))
    tb = cal_acc.get_tabs(test_infos)
    tb=cal_acc.summary_tb(tb,test_infos)
    txt_save_path=os.path.join(args.predict_dir,args.model_data.split(".")[0]+"_test_result")
    print(txt_save_path)
    cal_acc.save_tb_in_txt(txt_save_path,tb)
    cal_acc.save_tb_in_xml(txt_save_path,tb)



if __name__ == '__main__':
    main()