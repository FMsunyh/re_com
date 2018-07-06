from server.documents.common import *

# request_urls_post = api.doc(body=api.model('request_urls_post', {
#     'image_address': fields.List(fields.String(description='image address', required=True))
# }))

# request_urls_post = api.doc(body=api.model('request_urls_post', {
#     'image_address': fields.String(description='image address', required=True)
# }))
#
# request_data_post = api.doc(body=api.model('request_data_post', {
#     'data': fields.Nested(model=api.model('dict', {
#         'img_name': fields.String(description='The name of image', required=True),
#         'base64_code': fields.String(description='The base64 code of image', required=True),
#         'method': fields.Integer(description='method', required=True),
#         'rect': fields.Nested(model=api.model('rect', {
#             'x1':fields.Integer(description='x1', required=True),
#             'y1': fields.Integer(description='y1', required=True),
#             'x2': fields.Integer(description='x2', required=True),
#             'y2': fields.Integer(description='y2', required=True)
#         })),
#     }))
# }))


# request_urls_post = api.doc(body=api.model('request_urls_post', {
#     'data': fields.Nested(model=api.model('commdity_recognition', {
#         'image_address': fields.String(description='image address', required=False),
#         'base64_code': fields.String(description='image base64_code', required=False)}))
# }))

request_urls_post = api.doc(body=api.model('request_urls_post', {
    'data': fields.Nested(model=api.model('commdity_recognition', {
        'base64_code': fields.String(description='image base64_code', required=False)}))
}))

