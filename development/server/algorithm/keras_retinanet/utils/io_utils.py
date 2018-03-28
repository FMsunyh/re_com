#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 3/15/2018 4:22 PM 
# @Author : sunyonghai 
# @File : io_utils.py 
# @Software: ZJ_AI
# =========================================================

# 引入模块
import os
import shutil


def mkdir(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    is_exists = os.path.exists(path)

    # 判断结果
    if not is_exists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        try:
            os.makedirs(path)
        except Exception as e:
            print("Can't create dir:", path)

        print(path + ' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')
        return False

def move(src_file, obj_dir):
    mkdir(obj_dir)

    try:
        shutil.move(src_file, obj_dir)
        print('move successfuly')
    except Exception as e:
        print("Can't not move {} to {}. :{}", src_file, obj_dir, e)

def delete_file_folder(src):
    # 去除首位空格
    src = src.strip()
    # 去除尾部 \ 符号
    src = src.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    is_exists = os.path.exists(src)

    # 判断结果
    if not is_exists:
        return

    '''delete files and folders'''
    if os.path.isfile(src):
        try:
            os.remove(src)
        except:
            pass
    elif os.path.isdir(src):
        for item in os.listdir(src):
            itemsrc=os.path.join(src,item)
            delete_file_folder(itemsrc)
        try:
            os.rmdir(src)
        except:
            pass

def rename(oldname, newname):
    try:
        if oldname !='' and newname != '':
            os.rename(oldname, newname)
            print('old name:', oldname)
            print('new name:', newname)
    except Exception as ex:
        print(ex)





if __name__ == '__main__':
    delete_file_folder('/home/syh/temp/a')
