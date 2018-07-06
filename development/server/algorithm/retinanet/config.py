import os
# MAPPING_PATH = '/home/syh/commdity_recognition/development/server/algorithm/keras_retinanet/mapping_all.json'
import server.config

LABEL_MAPPING_PATH =os.path.join(server.ROOT_DIR, 'server/algorithm/retinanet/mapping_all.json')
MODEL_PATH = server.config.WEIGHT_PATH