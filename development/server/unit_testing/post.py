import sys
import json
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

host = 'http://192.168.1.184:16888/commdity_recognition/recognition'

def test():
    fn = 'test.json'
    data = get_data(fn)
    print(fn)
    print(json.dumps(data, indent=4))

    res = post(host, data)

    print('Request URL:', host)

    print('Response Body:')
    print(res.text)


def test_base64_code():
    fn = 'base64_code.json'
    data = get_data(fn)
    print(fn)
    print(json.dumps(data, indent=4))

    print('Request URL:', host)

    res = post(host, data)

    print('Response Body:')
    print(res.text)


def test_address():
    fn = 'address.json'
    data = get_data(fn)
    print(fn)
    print(json.dumps(data, indent=4))

    print('Request URL:', host)

    res = post(host, data)

    print('Response Body:')
    print(res.text)


if __name__ == "__main__":

    tic = time.time()

    # test()
    # test_base64_code()
    test_address()

    toc = time.time()

    print(str(1000 * (toc - tic)) + " ms")
