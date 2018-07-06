import multiprocessing.pool
import pprint
import sys
import json

import os
import requests
import time

sys.path.append("/home/syh/commdity_recognition/development")

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

host = 'http://192.168.1.210:16888/commdity_recognition/recognition'
# host = 'http://192.168.1.176:16888/commdity_recognition/recognition'
# host = 'http://121.8.142.254:16888/commdity_recognition/recognition'
# host = 'http://192.168.1.186:5000/predict/'
# host = 'http://{}:{}/commdity_recognition/recognition'.format(sconfig.HOST_IP, sconfig.PROT)

def test():
    fn = 'test.json'
    data = get_data(fn)
    print(fn)
    print(json.dumps(data, indent=4))

    res = post(host, data)

    print('Request URL:', host)

    print('Response Body:')
    pprint.pprint(res.text)


def test_base64_code():
    fn = 'test.json'
    data = get_data(fn)
    print(fn)
    print(json.dumps(data, indent=4))

    print('Request URL:', host)

    res = post(host, data)

    print('Response Body:')
    pprint.pprint(res.text)


def test_address():
    fn = 'address.json'
    data = get_data(fn)
    print(fn)
    # print(json.dumps(data, indent=4))

    print('Request URL:', host)

    res = post(host, data)

    print('Response Body:')
    pprint(res.text)


def run():
    tic = time.time()
    # test()
    test_base64_code()
    # test_address()
    toc = time.time()

    print(str(1000 * (toc - tic)) + " ms")


# if __name__ == "__main__":
#
#     p = multiprocessing.pool.Pool()
#     for i in range(100):
#         p.apply_async(run, args=())
#
#     p.close()
#     p.join()

if __name__ == "__main__":
    run()