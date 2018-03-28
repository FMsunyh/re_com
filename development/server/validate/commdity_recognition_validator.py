# encoding=utf-8

from server.status import build_result, APIStatus
from server import logger


def check_payload(ok, data):
    if ok:
        urls = data['payload']['image_address']
        for url in urls:
            cond1 = isinstance(url, str)

            if cond1:
                continue
            else:
                logger.debug("Wrong parameter: %s" % data)
                return False, build_result(APIStatus.BadRequest)

    return ok, data