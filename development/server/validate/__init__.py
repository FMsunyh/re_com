# encoding=utf-8

from functools import wraps


def check(*validators):

    def do_check(ok, data):
        final_ok, final_data = ok, data
        if ok:
            for validator in validators:
                if callable(validator):
                    final_ok, final_data = validator(final_ok, final_data)
        return final_ok, final_data

    def wrapper(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            ok, data = f(*args, **kwargs)
            return do_check(ok, data)
        return decorator

    return wrapper