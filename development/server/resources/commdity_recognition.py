from flask_restplus.resource import Resource
from server import api
from server.resources.common import add_root, add_payload, add_args

import server.documents.commdity_recognition_doc as documents
import server.services as services
import server.validate as validators
from server.validate.commdity_recognition_validator import check_payload

class CommdityRecognition(Resource):

    @services.commdity_recognition_decorator.recognition
    @documents.request_urls_post
    @validators.check(check_payload)
    def post(self):
         return add_payload(*add_root())

class CommdityRecognitionFRNN(Resource):

    @services.commdity_recognition_decorator.recognition_frnn
    @documents.request_urls_post
    # @validators.check(check_payload)
    def post(self):
         return add_payload(*add_root())

ns = api.namespace(name="commdity_recognition", description='commdity recognition interface')
ns.add_resource(CommdityRecognition, '/recognition')
# ns.add_resource(CommdityRecognition, '/fast_moving_recognition')
# ns.add_resource(CommdityRecognitionFRNN, '/recognition_frcnn')