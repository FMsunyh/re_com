import os
# MAPPING_PATH = '/home/syh/commdity_recognition/development/server/algorithm/keras_retinanet/mapping_all.json'
from server.config import ROOT_DIR,WEIGHT_PATH

LABEL_MAPPING_PATH =os.path.join(ROOT_DIR, 'server/algorithm/retinanet/mapping_all.json')
MODEL_PATH = WEIGHT_PATH
LOAD_MODEL=False