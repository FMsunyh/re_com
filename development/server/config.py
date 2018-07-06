# encoding=utf-8
import os

LOG_CONFIG = {
    'level': 'DEBUG',
    'filename': 'server.log'
}

import socket
HOST_NAME = socket.getfqdn(socket.gethostname()) == 'zjai-dev-007'

ROOT_DIR = '/home/syh/commdity_recognition/development/'

OUTPUT_DIR = os.path.join(ROOT_DIR, 'server/static/images/')
DOWNLOAD_DIR = os.path.join(ROOT_DIR, 'server/data/download/')

HOST_IP = '192.168.1.184'
# HOST_IP = '192.168.1.196'
PROT = '16888'
print('run -----')