#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 7/6/2018 17:26 AM
# @Author : jaykky
# @File : zjai_3_checkData.py
# @Software: ZJ_AI
#此程序是用于检查数据是否缺失，以及统计每个label的分布情况。
#属于构造fasterrcnn的数据集的步骤三
#输入：Annotation文件夹的父路径，以及数据类型（trainval && test）
#输出：数据中每个label的分布情况统计信息 txt文件
# =========================================================

import os.path as osp
import xml.etree.ElementTree as ET



def get_txt_data(dir,type):
    '''
    函数用于读取数据图像名称列表的txt文件（如ImageSets/Main文件夹下的test.txt）
    :param dir:文件所在的路径
    :param type:文件名称，不需要后缀名
    :return:xml清单
    '''
    fileDir=dir+"/ImageSets/Main/"+type+".txt"
    dataList=[]
    with open(fileDir,'r') as f:
        lineList=f.readlines()
        for line in lineList:
            line=line.replace("\n","")
            dataList.append(line)
    return dataList

def check_xml(xmlPath,labelCount):
    '''
    函数用于读取xml文件中含有label类型和个数
    :param xmlPath:xml文件的路径
    :param labelCount:每个label的种类和个数
    :return:更新后的label分布情况
    '''
    et = ET.parse(xmlPath)
    element = et.getroot()
    element_objs = element.findall('object')

    for element_obj in element_objs:
        node = element_obj.find('name')
        label=node.text
        if label in list(labelCount.keys()):
            labelCount[label]+=1
        else:
            labelCount[label]=1
    return labelCount


def get_all_xml(dirs,annot_Path):
    '''
    函数用于统计所有xml中所有label的分布情况
    :param dirs:xml文件名称
    :param annot_Path:xml文件的父路径
    :return:所有label的分布情况
    '''
    labelCount={}
    count=0
    for dir in dirs:
        # fileDict=get_dict(annot_Path)
        xmlPath=osp.join(annot_Path,"Annotations",dir+".xml")
        xmlPath=xmlPath.replace("JPEGImages","Annotations")
        labelCount=check_xml(xmlPath,labelCount)
        count+=1
        if count%5000==0:
            print(count)
    # print(labelCount)
    return labelCount

# def IsValidXml(dirs):
#     '''
#     函数用于批量检查xml中是否存在不含有object的情况
#     :param dirs:xml文件的父路径
#     :return:
#     '''
#     for dir in os.listdir(dirs):
#         num=checkValidXml(dirs+"/"+dir)
#         if num==0:
#             print(dirs)

def count_label(labelCount):
    '''
    统计所有object个数
    :param labelCount:label的分布情况
    :return:object个数
    '''
    count = 0
    for value in list(labelCount.values()):
        count += value
    print(count)
    return count

def write_label_count(dataSetDir,labelCount,type):
    '''
    函数用于将完整的label分布情况写入到txt文件中
    :param dataSetDir: 写入txt文件的路径
    :param labelCount: label的分布情况
    :param type: txt文件名
    :return:
    '''
    count=count_label(labelCount)
    with open(dataSetDir+"/"+"labelCount_{}.txt".format(type),"w") as f:
        for label in list(labelCount.keys()):
            f.write(label+" :  "+str(labelCount[label])+"\n")
        f.write("total have {} type object\n".format(str(len(labelCount.values()))))
        f.write("total have {} objects\n".format(str(count)))
    print("finish")

def get_dict(dataDirs):
    fileDict={}
    with open(dataDirs+"/ImageSets/Main/filedict.txt","r") as f:
        lineList=f.readlines()
        for line in lineList:
            key,value=line.replace("\n","").split("|")
            fileDict[key]=value
    return fileDict



def write_label_count1(root_dir,labelCount,type):
    '''
        函数用于将完整的label分布情况写入到txt文件中
        :param dataSetDir: 写入txt文件的路径
        :param labelCount: label的分布情况
        :param type: txt文件名
        :return:
    '''
    count=count_label(labelCount)
    sortDict=sorted(labelCount.items(),key = lambda x:x[1],reverse = False)
    min=""
    max=""
    with open(root_dir+"/"+"labelCount_{}.txt".format(type),"w") as f:
        dictNum=len(sortDict)
        countNum=0
        for key, value in sortDict:
            # print(key,value)
            if count==0:
                min=key
            if count==dictNum-1:
                max=key
            f.write(key+" :  "+str(value)+"\n")
            countNum+=1
        f.write("total have {} type object\n".format(str(len(labelCount.values()))))
        f.write("total have {} objects\n".format(str(count)))
        # f.write("{} type object have only ".format(str(min))+"{} \n".format(str(sortDict[min])))
        # f.write("{} type object have only ".format(str(max)) + "{} \n".format(str(sortDict[max])))
    print("finish")

def analysis_data(root_dir,fileType):
    txtData = get_txt_data(root_dir, fileType)
    labelCount = get_all_xml(txtData, root_dir)
    write_label_count1(root_dir, labelCount, fileType)

if __name__=="__main__":
    root_dir=osp.abspath(osp.join(osp.dirname(__file__), '..'))
    dataDirs = osp.join(root_dir, 'data', 'test_data')
    dataDirs = '/home/hyl/data/ljk/github-pro/zjai-com/data/train_data/train_data-2018-08-15_resize'
    root_dir = dataDirs
    type="trainval"
    txtData=get_txt_data(dataDirs,type)
    labelCount=get_all_xml(txtData,dataDirs)
    write_label_count1(root_dir,labelCount,type)
