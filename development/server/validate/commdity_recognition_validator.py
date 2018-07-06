# encoding=utf-8

from server.status import build_result, APIStatus
from server import logger

def is_base64_code(s):
    '''Check s is Base64.b64encode'''
    if not isinstance(s ,str) or not s:
        return False

    _base64_code = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
                    'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                    'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a',
                    'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                    'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                    't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1',
                    '2', '3', '4','5', '6', '7', '8', '9', '+',
                    '/', '=' ]

    # Check base64 OR codeCheck % 4
    code_fail = [ i for i in s if i not in _base64_code]
    if code_fail or len(s) % 4 != 0:
        return False
    return True

def check_payload(ok, data):
    if ok:
        str_code = data['payload']['data']['base64_code']

        if ',' not in str_code:
            logger.debug("Wrong parameter: %s" % data)
            return False, build_result(APIStatus.BadRequest)

        base64_code = str_code.split(',')[1]
        cond1 = is_base64_code(base64_code)

        if not cond1:
            logger.debug("Wrong parameter: %s" % data)
            return False, build_result(APIStatus.BadRequest)

    return ok, data