from http.client import OK
from flask import request, abort
from flask_restful import Resource
from marshmallow import Schema, fields

from ..utils.auth import adm_required

from ..service.user import create_user, delete_user, get_all_users, get_user_by_id, update_user

# For comment body parsing
class UserBodySchema(Schema):
    id = fields.Int(required = False, help = "Identification of the user")
    name = fields.Str(required = True, help = "name must be provided")
    password = fields.Str(required = True, help = "password must be provided")
    is_adm = fields.Bool(required = True, help = "is_adm must be provided")


# Parser instances
body_parser = UserBodySchema()


class UserRoute(Resource):
    @adm_required
    def get(current_user, self, id = None):
        if id == None:
            return get_all_users(), OK
        else:
            return get_user_by_id(id), OK
    
    @adm_required
    def post(current_user, self):
        errors = body_parser.validate(request.json)
        if errors:
            abort(400, str(errors))
        
        body = body_parser.load(request.json)

        return create_user(body), OK

    @adm_required
    def put(current_user, self):
        errors = body_parser.validate(request.json)
        if errors:
            abort(400, str(errors))
        
        body = body_parser.load(request.json)

        return update_user(body), OK

    @adm_required
    def delete(current_user, self, id = None):
        if id == None:
            abort(400, "Id must be provided for this kind of operation.")

        return delete_user(id), OK
