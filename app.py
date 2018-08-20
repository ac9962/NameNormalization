from flask import Flask
from flask_zipkin import Zipkin
from flask_restplus import Api, Resource
from model.response import resp_resource
from model.req_parser_model import MemberName_schema

app = Flask(__name__)
api = Api(app)
req_post = api.model('post_req', resp_resource)

@api.route('/normalize')
class Index(Resource):
    @api.expect(req_post)
    def post(self):
        memschema = MemberName_schema()
        req_payload = memschema.load(api.payload)
        if len(req_payload.errors) > 0:
            return {'error': "Required field 'name' is missing"}, 406
        elif len(req_payload.data['name']) == 0 or len(req_payload.data['name']) is None:
            return {'error': "Missing data for field 'name' cannot be null"}, 400
        return req_payload.data, 201


if __name__ == '__main__':
    app.run(debug=False)