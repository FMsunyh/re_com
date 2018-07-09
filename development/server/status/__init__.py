# encoding=utf-8


class HTTPStatus:
    # Success
    Ok = 200

    # Argument Error
    BadRequest = 400

    # Authentication failed
    UnAuthorized = 401

    # Forbidden access
    Forbidden = 403

    # Not found
    NotFound = 404

    # Internal server Error
    InternalServerError = 500

    # Service unavailable
    ServiceUnavailable = 503


class APIStatus:
    Ok = 100000

    BadRequest = 100001

    InternalServerError = 100002

    Forbidden = 100003

    NotFound = 100404

    # Descriptions = {
    #     Ok: '成功',
    #     NotFound: '未找到该资源',
    #     BadRequest: '请求参数有误',
    #     InternalServerError: '服务器内部错误',
    #     Forbidden: '拒绝该请求',
    # }

    Descriptions = {
        Ok: 'success',
        NotFound: 'Not Find The Resource',
        BadRequest: 'Bad Request',
        InternalServerError: 'Internal Server Error',
        Forbidden: 'Forbidden Request',
    }


def to_http_status(status):
    return {
        APIStatus.Ok: HTTPStatus.Ok,
        APIStatus.BadRequest: HTTPStatus.BadRequest,
        APIStatus.InternalServerError: HTTPStatus.InternalServerError,
        APIStatus.Forbidden: HTTPStatus.Forbidden,
        APIStatus.NotFound: HTTPStatus.NotFound,
    }[status]


def build_result(status, data=None):
    if data is not None:
        return {'status': status, 'msg': APIStatus.Descriptions[status], 'data': data}
    return {'status': status, 'msg': APIStatus.Descriptions[status]}