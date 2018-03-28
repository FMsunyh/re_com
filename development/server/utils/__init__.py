from functools import wraps

def _build_decorator_generator(func):
    def wrapper(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            return func(f, *args, **kwargs)
        return decorator
    return wrapper

def _build_passing_decorator_func(func):
    def wrapper(continuation, *args, **kwargs):
        ok, response = continuation(*args, **kwargs)
        return func(ok, response)
    return wrapper


def build_passing_decorator_class(methods, name, impl):
    meta_methods = {}
    for method in methods:
        func = getattr(impl, method, None)
        if func:
            meta_methods.update({method: _build_decorator_generator(_build_passing_decorator_func(func))})
    return type(name, (object, ), meta_methods)
