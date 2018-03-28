import os
import tensorflow as tf

os.environ["CUDA_VISIBLE_DEVICES"] = ""


def get_session():
    cfg = tf.ConfigProto()
    # cfg.gpu_options.allocator_type = 'BFC'
    # cfg.gpu_options.per_process_gpu_memory_fraction = 0.90
    cfg.gpu_options.allow_growth = True
    return tf.Session(config=cfg)

def set_cpu():
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"

    #
    # sess = get_session()
    #
    # import keras.backend.tensorflow_backend as ktf
    # ktf.set_session(sess)

    # os.environ["CUDA_VISIBLE_DEVICES"] = ""

import time
from functools import wraps


def fn_timer(fp):

    @wraps(fp)
    def function_timer(*args, **kwargs):
        t0 = time.time()
        result = fp(*args, **kwargs)
        t1 = time.time()
        print("Total time running %s: %s ms" % (fp.__name__, str(1000 * (t1 - t0))))
        return result

    return function_timer

