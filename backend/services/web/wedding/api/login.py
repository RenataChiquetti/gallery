from http.client import OK
from flask import request, abort
from flask_restful import Resource
from marshmallow import Schema, fields

from ..utils.auth import auth, check_auth

# For comment body parsing
class LoginBodySchema(Schema):
    name = fields.Str(required = True, help = "name must be provided")
    password = fields.Str(required = True, help = "password must be provided")


# Parser instances
body_parser = LoginBodySchema()


class LoginRoute(Resource):
    def get(self):
        return check_auth()
        
    def post(self):
        errors = body_parser.validate(request.json)
        if errors:
            abort(400, str(errors))
        
        body = body_parser.load(request.json)

        return auth(body["name"], body["password"])
