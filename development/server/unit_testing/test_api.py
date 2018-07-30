# -*- coding: utf-8 -*-
# @Time    : 5/17/2018 11:01 AM
# @Author  : sunyonghai
# @File    : test_api.py
# @Software: ZJ_AI
import multiprocessing.pool
import pprint
import json
import requests
import time

def get_data(json_file):
    with open(json_file) as data_file:
        data = json.load(data_file)
        # print(data)
    return data

def post(url, data):
    if url == '':
        return None

    res = requests.post(url, json=data)
    return res

# host = 'http://192.168.1.015:16888/commdity_recognition/recognition'
host = 'http://192.168.1.210:16888/commdity_recognition/recognition_frcnn'
# host = 'http://121.8.142.254:16888/commdity_recognition/recognition'
# host = 'http://192.168.1.176:16888/commdity_recognition/recognition'


def test_base64_code():
    fn = 'test.json'
    data = get_data(fn)
    print('data file: {}'.format(fn))
    # print(json.dumps(data, indent=4))
    print('Request URL:', host)

    res = post(host, data)

    print('Response Body(return value):')
    pprint.pprint(res.text)

def test_api():
    fn = 'test.json'
    data = get_data(fn)
    print('data file: {}'.format(fn))
    # print(json.dumps(data, indent=4))
    print('Request URL:', host)

    res = post(host, data)

    print('Response Body(return value):')
    pprint.pprint(res.text)

def run():
    tic = time.time()
    test_api()
    toc = time.time()

    print('proccess time: {}'.format(str(1000 * (toc - tic)) + " ms"))

# if __name__ == "__main__":
#     p = multiprocessing.pool.Pool()
#     for i in range(20):
#         p.apply_async(run, args=())
#     p.close()
#     p.join()

if __name__ == "__main__":
    run()

"""
cd ../unit_testing
python test_api.py
"""