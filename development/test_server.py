# -*- coding: utf-8 -*-
# @Time    : 5/17/2018 11:01 AM
# @Author  : sunyonghai
# @File    : test_api.py
# @Software: ZJ_AI
import argparse
import json
import pprint
import time

import requests
parser = argparse.ArgumentParser(description='Get the data info')
parser.add_argument('-ip', '--host',help='IP address of server', default='')
parser.add_argument('-p', '--port',help='Port', default='16888')
args = parser.parse_args()

def host_interface():
    if args.host:
        api_str = 'http://'+args.host+':'+args.port+'/commdity_recognition/recognition'

    return api_str

host = host_interface()

def get_data(json_file):
    with open(json_file) as data_file:
        data = json.load(data_file)
    return data

def post(url, data):
    if url == '':
        return None
    res = requests.post(url, json=data)
    return res

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


if __name__ == "__main__":
    run()

"""
cd ../unit_testing
python test_api.py
"""