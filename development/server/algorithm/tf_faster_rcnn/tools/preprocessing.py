# -----------------------------------------------------
# -*- coding: utf-8 -*-
# @Time    : 8/9/2018 4:34 PM
# @Author  : sunyonghai
# @Software: ZJ_AI
# -----------------------------------------------------
import logging

import datasets.factory
import model.train_val
from model.config import cfg,cal_data_aug_code
import os
import pickle

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def combined_roidb(imdb_name):
    logger.warning("{}".format('The `combined_roidb` function is deprecat and will be removed after 08/2018. Use instead `calc_roidb`'))
    return calc_roidb(imdb_name)

def wrote_roidbs(roidb,imdb_name,roidb_file):
    # roidb_file=os.path.join(cfg.ROOT_DIR,"data","cache",'{}_enhance_roidb.pkl'.format(imdb_name))
    with open(roidb_file, 'wb') as fid:
        pickle.dump(roidb, fid, pickle.HIGHEST_PROTOCOL)
    print('wrote enhance {}roidb to {}'.format(imdb_name,roidb_file))


def calc_roidb(imdb_name,package_name):
    imdb = datasets.factory.get_imdb(imdb_name,package_name)
    logger.info('Loaded dataset `{:s}` for training'.format(imdb.name))
    imdb.set_proposal_method(cfg.TRAIN.PROPOSAL_METHOD)

    logger.info('Set proposal method: {:s}'.format(cfg.TRAIN.PROPOSAL_METHOD))
    postfix = cal_data_aug_code(cfg)
    roidb_file = os.path.join(cfg.ROOT_DIR, "data", "cache", '{}_{}_enhance_roidb_{}.pkl'.format("+".join(package_name),imdb_name,postfix))

    if os.path.exists(roidb_file)!=1:
        roidb = model.train_val.get_training_roidb(imdb)
        wrote_roidbs(roidb, imdb_name,roidb_file)
        return imdb, roidb
    else:
        with open(roidb_file, 'rb') as fid:
            try:
                roidb = pickle.load(fid)
            except:
                roidb = pickle.load(fid, encoding='bytes')
        print('{} gt roidb loaded from {}'.format(imdb_name, roidb_file))
        return imdb,roidb
