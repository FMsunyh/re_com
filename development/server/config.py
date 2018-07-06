# encoding=utf-8
import os

LOG_CONFIG = {
    'level': 'DEBUG',
    'filename': 'server/log/server.log'
}

import socket
# HOST_NAME = socket.getfqdn(socket.gethostname()) == 'zjai-dev-007'

# ROOT_DIR = '/home/syh/commdity_recognition/development/'
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

OUTPUT_DIR = os.path.join(ROOT_DIR, 'server','static','images')
DOWNLOAD_DIR = os.path.join(ROOT_DIR, 'server', 'static', 'download')
WEIGHT_PATH = os.path.join(ROOT_DIR, 'server', 'weights','rel_weight.h5')