# encoding=utf-8
import os

MYSQL_CONFIG = {
    'maxConnections': 5,
    'minFreeConnections': 2,
    'host': '172.31.100.168',
    'port': 3306,
    'user': 'user_ai1',
    'password': '6wkGB7J8R',
    'database': 'AI',
    'charset': 'utf8mb4',
}



LOG_CONFIG = {
    'level': 'DEBUG',
    'filename': './server/server.log'
}

import socket
HOST_NAME = socket.getfqdn(socket.gethostname()) == 'zjai-dev-007'

# if HOST_NAME:
#     ES_HOST = ['192.168.38.252']
#     OUTPUT_DIR = '/home/syh/trunk/commdity_recognition/development/server/static/download/'
#     DOWNLOAD_DIR = '/home/syh/trunk/commdity_recognition/development/server/static/download/'
#
# else:
#     # 168 server
#     # ES_HOST = ['172.31.100.195', '172.31.100.169']
#     ES_HOST = ['172.31.100.195']
#     OUTPUT_DIR = '/data/commdity_recognition/download/'
#     DOWNLOAD_DIR = '/data/commdity_recognition/download/'

ROOT_DIR = '/home/syh/commdity_recognition/development/'

OUTPUT_DIR = os.path.join(ROOT_DIR, 'server/static/images/')
DOWNLOAD_DIR = os.path.join(ROOT_DIR, 'server/data/download/')
