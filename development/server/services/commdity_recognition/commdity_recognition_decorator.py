# coding: utf-8
# import所需模块
import base64
import os
import shutil
import time
import uuid
from io import BytesIO

import cv2
import requests
from PIL import Image

from server.algorithm.keras_retinanet.bin.predict import predict, visualize, get_class_count
from server import logger
from server.config import DOWNLOAD_DIR, OUTPUT_DIR
from server.services.commdity_recognition.model import ImageInfo
from server.status import build_result, APIStatus, to_http_status
from server.utils import build_passing_decorator_class
from server.algorithm.keras_retinanet.utils.image import read_image_bgr


class CommdityRecognitionImp(object):

    @staticmethod
    def recognition(ok, source):
        try:
            if ok:

                tic = time.time()
                img_url = CommdityRecognitionImp.get_urls(source)
                image_path, file_name = CommdityRecognitionImp.get_image(source)

                if image_path != '':
                    imageinfo = CommdityRecognitionImp.create_imageinfo(file_name=file_name)
                    imageinfo.path = image_path

                elif img_url != '':
                    imageinfo = CommdityRecognitionImp.create_imageinfo(url=img_url)
                    imageinfo.address = img_url
                    CommdityRecognitionImp.download_image(imageinfo, output_dir=DOWNLOAD_DIR)


                print('start processing.............................................')
                # 1. get image
                image = read_image_bgr(imageinfo.path)
                # copy to draw on
                draw = image.copy()
                draw = cv2.cvtColor(draw, cv2.COLOR_BGR2RGB)

                # 2. predict
                predicted_labels, scores, detections = predict(image)

                data = get_class_count(predicted_labels, scores)

                # make the return data
                im_draw = visualize(draw, predicted_labels, scores, detections)

                im = Image.fromarray(im_draw)
                im_path = os.path.join(OUTPUT_DIR, str(imageinfo.name)+imageinfo.image_extension)
                im.save(im_path)

                # res = yoins_search(classify=classify_name, query_fea_str=query_image)
                #
                # # res = test_search("")
                # data = dict()
                # for i, item in enumerate(res):
                #     data[str(i)] = item
                # # data = {"1": "1.jpg"}

                toc = time.time()
                print(str(1000 * (toc-tic)) + " ms")

                out_path = '{}{}{}'.format('192.168.1.184:16888', '/static/images/',str(imageinfo.name) + imageinfo.image_extension)
                # print(out_path)
                data['address'] = out_path
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
    def download_images(img_urls, output_dir=''):

        images = []
        for url in img_urls:
            namespace_dns = uuid.UUID('6ba7b810-9dad-11d1-80b4-00c04fd430c8')
            file_name = uuid.uuid3(namespace_dns, url)
            image = ImageInfo(file_name, url)
            images.append(image)
            CommdityRecognitionImp.download_image(image, output_dir)

        return images

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
    def download_image(image, output_dir=''):
        try:
            if not os.path.exists(output_dir):
                logger.warning('%s, This folder is not exist, it will be create.', output_dir)
                os.makedirs(output_dir)

            # file_suffix = os.path.splitext(image.address)[1]

            image_path = '{}{}{}{}'.format(output_dir, os.sep, image.name, image.image_extension)

            all_format = ['jpg']
            img_format = image.address.split(".")[-1]
            if img_format.lower() not in all_format:
                print('not a valid image')
                raise Exception

            ir = requests.get(image.address)
            with open(image_path, 'wb') as fp:
                fp.write(ir.content)
                image.path = image_path
                logger.debug('download the image:%s' % image.address)
        except IOError as e:
            logger.error('File operation error: %s', e, exc_info=True)
        except Exception as e:
            logger.error('Error: %s', e, exc_info=True)

    @staticmethod
    def get_image(image_msg):
        base64_code = image_msg['payload']['data']['base64_code']
        if base64_code =='':
            return '', ''

        # code = base64_code.json[23:]
        code = base64_code.split(',')[1]
        suffix = base64_code.split(',')[0].split(';')[0].split('/')[1]

        image = base64.b64decode(code)
        img = Image.open(BytesIO(image))

        file_name = uuid.uuid1()
        image_path = '%s%s%s%s' % (DOWNLOAD_DIR, file_name, '.', suffix)
        CommdityRecognitionImp.im_save(image_path, img)

        print("file name:", file_name)
        print("image path:", image_path)
        return image_path, file_name

    @staticmethod
    def get_image_from_base64(image_msg):
        base64_code = image_msg['payload']['data']['base64_code']
        if base64_code == '':
            return '', '', ''

        code = base64_code.split(',')[1]
        suffix = base64_code.split(',')[0].split(';')[0].split('/')[1]

        image = base64.b64decode(code)
        img = Image.open(BytesIO(image))

        file_name = uuid.uuid1()
        image_path = '%s%s%s%s' % (DOWNLOAD_DIR, file_name, '.', suffix)
        # CommdityRecognitionImp.im_save(image_path, img)
        #
        # print("file name:", file_name)
        # print("image path:", image_path)
        return image_path, file_name,img

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


commdity_recognition_decorator = build_passing_decorator_class(['recognition'], 'commdity_recognition_decorator', CommdityRecognitionImp)
