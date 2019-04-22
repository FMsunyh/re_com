# coding: utf-8
# import所需模块
import base64
import datetime
import os
import shutil
import time
import uuid
from io import BytesIO

import cv2
import requests
from PIL import Image

from server.algorithm.tf_faster_rcnn.morelib.bin.predict_test import predict_frnn
from server.algorithm.retinanet.bin.predict import predict, visualize, get_prediect_label_bbox
from server import logger
from server.config import DOWNLOAD_DIR, OUTPUT_DIR
from server.services.commdity_recognition.model import ImageInfo
from server.status import build_result, APIStatus, to_http_status
from server.utils import build_passing_decorator_class
from server.algorithm.retinanet.utils.image import read_image_bgr

import numpy as np

import server.config

USE_FRNN = True

global request_count
request_count = 0

class CommdityRecognitionImp(object):

    @staticmethod
    def recognition(ok, source):
        if USE_FRNN:
            return CommdityRecognitionImp.recognition_frnn(ok, source)
        else:
            return CommdityRecognitionImp.recognition_RetinaNet(ok, source)

    @staticmethod
    def recognition_RetinaNet(ok, source):
        try:
            if ok:
                tic = time.time()
                print('start processing.............................................')

                # 1. get image
                image =  CommdityRecognitionImp.get_image_from_base64(source)

                # 2. predict
                boxes, scores, labels = predict(image)
                # boxes, scores, labels = (1,1,1)
                data = get_prediect_label_bbox(boxes, scores, labels)

                toc = time.time()
                print("Request time: "+str(1000 * (toc - tic)) + " ms")
                print(data)
                return build_result(APIStatus.Ok, data=data), to_http_status(APIStatus.Ok)
            else:
                return source, to_http_status(source['status'])

        except Exception as e:
            logger.error('occur error: %s', e, exc_info=True)
            return build_result(APIStatus.InternalServerError), to_http_status(APIStatus.InternalServerError)

    @staticmethod
    def recognition_frnn(ok, source):
        try:
            if ok:
                tic = time.time()
                print('start processing.............................................')

                # 1. get image
                image = CommdityRecognitionImp.get_image_from_base64(source)

                # 2. predict
                data = predict_frnn(image)

                toc = time.time()
                print("Request time: " + str(1000 * (toc - tic)) + " ms")
                print(data)
                return build_result(APIStatus.Ok, data=data), to_http_status(APIStatus.Ok)
            else:
                return source, to_http_status(source['status'])

        except Exception as e:
            logger.error('occur error: %s', e, exc_info=True)
            return build_result(APIStatus.InternalServerError), to_http_status(APIStatus.InternalServerError)

    @staticmethod
    def get_urls(source):
        urls = source['payload']['data']['image_address']
        if urls != '':
            logger.debug("The request data:%s" % urls)
        return urls

    @staticmethod
    def create_imageinfo(url='', file_name=''):
        if url != '':
            namespace_dns = uuid.UUID('6ba7b810-9dad-11d1-80b4-00c04fd430c8')
            file_name = uuid.uuid3(namespace_dns, url)
        elif file_name != '':
            file_name = file_name

        image = ImageInfo(file_name)

        return image

    @staticmethod
    def get_image_from_base64(image_msg):
        base64_code = image_msg['payload']['data']['base64_code']
        code = base64_code.split(',')[1]

        image = base64.b64decode(code)
        img = Image.open(BytesIO(image))

        img_b64decode = image


        # file_name = uuid.uuid1()
        global request_count
        request_count += 1
        file_name = str(request_count)
        cur_date = datetime.datetime.now()
        str_date = '{year}-{month}-{day}'.format(year=cur_date.year, month=cur_date.month, day=cur_date.day)
        dir = os.path.join(DOWNLOAD_DIR, str_date)

        if not os.path.exists(dir):
            os.makedirs(dir)
            request_count = 0

        image_path = os.path.join(dir,  file_name+'.'+'jpg')
        print(image_path)
        with open(image_path, 'wb') as f:
            f.write(img_b64decode)


        # img = Image.fromarray(img.astype('uint8'))
        # img = Image.fromarray(img, mode='RGB')
        # CommdityRecognitionImp.im_save(image_path, img)

        img = np.asarray(img.convert('RGB'))

        print(img.shape)
        return img[:, :, ::-1].copy()

    # @staticmethod
    # def get_image_from_base64(image_msg):
    #     base64_code = image_msg['payload']['data']['base64_code']
    #     code = base64_code.split(',')[1]
    #
    #     image = base64.b64decode(code)
    #     img = Image.open(BytesIO(image))
    #
    #     # img_b64decode = base64.b64decode(code)
    #     # img = np.fromstring(img_b64decode, np.uint8)
    #
    #     # file_name = uuid.uuid1()
    #     global request_count
    #     request_count += 1
    #     file_name = str(request_count)
    #     cur_date = datetime.datetime.now()
    #     str_date = '{year}-{month}-{day}'.format(year=cur_date.year, month=cur_date.month, day=cur_date.day)
    #     dir = os.path.join(DOWNLOAD_DIR, str_date)
    #
    #     if not os.path.exists(dir):
    #         os.makedirs(dir)
    #         request_count = 0
    #
    #     image_path = os.path.join(dir, file_name + '.' + 'jpg')
    #     print(image_path)
    #     CommdityRecognitionImp.im_save(image_path, img)
    #
    #     img = np.asarray(img.convert('RGB'))
    #
    #     print(img.shape)
    #     return img[:, :, ::-1].copy()
    #
    @staticmethod
    def im_save(path, image):
        ret = -1
        try:
            if image is not None and path != '':
                ret = image.save(path)
        except Exception as ex:
            ret = -2
            # print(ex)
            logger.error('occur error: %s', ex, exc_info=True)
        else:
            pass
        finally:
            pass

        return ret

    @staticmethod
    def remove_all(path):
        try:
            file_list = os.listdir(path)
            for f in file_list:
                filepath = os.path.join(path, f)
                if os.path.isfile(filepath):
                    os.remove(filepath)
                    print(filepath + " removed!")
                elif os.path.isdir(filepath):
                    shutil.rmtree(filepath, True)
                    print("dir " + filepath + " removed!")

        except IOError as exc:
            print(exc)


commdity_recognition_decorator = build_passing_decorator_class(['recognition','recognition_frnn'], 'commdity_recognition_decorator', CommdityRecognitionImp)
