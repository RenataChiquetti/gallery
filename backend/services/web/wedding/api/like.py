from http.client import OK
from flask import request, abort
from flask_restful import Resource
from marshmallow import Schema, fields

from ..utils.auth import login_required

from ..service.like import check_like, check_like_by_post, like

# For comment body parsing
class LikeBodySchema(Schema):
    post_id = fields.Int(required = True, help = "post_id must be provided")


# Parser instances
body_parser = LikeBodySchema()

class LikeRoute(Resource):
    @login_required
    def get(current_user, self, post_id = None, like_post_id = None):
        if post_id == None:
            return check_like(current_user["id"], like_post_id), OK
        elif like_post_id == None:
            return check_like_by_post(post_id), OK
            
    @login_required
    def post(current_user, self):
        errors = body_parser.validate(request.json)
        if errors:
            abort(400, str(errors))
   
        body = body_parser.load(request.json)

        return like(current_user["id"], body["post_id"]), OK
