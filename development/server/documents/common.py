from flask_restplus import reqparse
from flask_restplus import fields

from server import api
from server.status import APIStatus, to_http_status


def build_response(name, data):
    return api.response(code=to_http_status(APIStatus.Ok), model=api.model(name, {
                     'status': fields.Integer(description='返回状态码'),
                     'msg': fields.String(description='返回状态信息'),
                     'data': fields.Nested(model=data, description='返回的数据')
                 }), description='返回内容')


request_parser = reqparse.RequestParser()
request_parser.add_argument('token', type=str, required=True, location='headers')
request_token = api.expect(request_parser, validate=True)
