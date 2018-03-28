# encoding=utf-8

import logging
import logging.handlers

from flask import Flask
from flask_restplus import Api

from server.config import LOG_CONFIG


def __create_logger(conf):
    """
    :param conf: log config
    :return: logger object
    """

    logger_ = logging.getLogger('model-detection-service')
    logger_.setLevel(conf['level'])

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(
        logging.Formatter('%(asctime)s [%(pathname)s:%(lineno)d:%(funcName)s] %(message)s'))
    stream_handler.setLevel(conf['level'])
    logger_.addHandler(stream_handler)

    file_handler = logging.handlers.TimedRotatingFileHandler(conf['filename'], when='D', encoding='utf-8')
    file_handler.setFormatter(
        logging.Formatter('%(asctime)s [%(pathname)s:%(lineno)d:%(funcName)s] %(message)s'))
    file_handler.setLevel(conf['level'])
    logger_.addHandler(file_handler)

    return logger_


logger = __create_logger(LOG_CONFIG)

# Flask API Object
app = Flask(__name__,
            static_folder='static',
            template_folder='static/client')

app.config['SECRET_KEY'] = 'development'

api = Api(app, version='beta', title='商品识别', description='识别图片中的商品', authorizations={}, ui=True)

from server.resources import *

