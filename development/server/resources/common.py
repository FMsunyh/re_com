from flask import request
from server import logger
from server.status import build_result, APIStatus


def add_root(**kwargs):
    return True, kwargs


def add_payload(ok, data):
    if ok:
        try:
            # print(request.data)
            payload = request.json
            # print(payload)
            data['payload'] = payload
            # print(data['payload'].keys())
            return  True, data
        except Exception as e:
            logger.error('Occurred a error when added payload £º%s', e, exc_info=True)
            return False, build_result(APIStatus.InternalServerError)
    return ok, data


def add_args(ok, args, arg_list):
    if ok:
        try:
            args['args'] = {}
            for arg in arg_list:
                args['args'][arg] = request.args[arg]
        except Exception as e:
            logger.error('Occurred a error when added args£º%s', e, exc_info=True)
            return False, build_result(APIStatus.BadRequest)
    return ok, args

