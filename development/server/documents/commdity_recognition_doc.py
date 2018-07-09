from server.documents.common import *
request_urls_post = api.doc(body=api.model('request_urls_post', {
    'data': fields.Nested(model=api.model('commdity_recognition', {
        'base64_code': fields.String(description='image base64_code', required=False)}))
}))

