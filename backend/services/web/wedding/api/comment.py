from http.client import OK
from flask import request, abort
from flask_restful import Resource
from marshmallow import Schema, fields

from ..utils.auth import adm_required, login_required

from ..service.comment import create_comment, delete_comment, get_all_comments, get_comment_by_id, update_comment, get_comments_by_post_id

# For url parameters validation
class CommentQuerySchema(Schema):
    post_id = fields.Str(required = True, help = "post_id is a required field")

# For comment body parsing
class CommentBodySchema(Schema):
    id = fields.Int(required = False, help = "Identification of the comment")
    content = fields.Str(required = True, help = "content must be provided")
    user_id = fields.Int(required = True, help = "user_id must be provided")
    post_id = fields.Int(required = True, help = "post_id must be provided")

# Parser instances
body_parser = CommentBodySchema()
query_parser = CommentQuerySchema()

class CommentsRoute(Resource):

    @login_required
    def get(current_user, self, id = None):
        if id == None:
            errors = query_parser.validate(request.args)

            if errors:
                return get_all_comments(), OK
            else:
                query = query_parser.load(request.args)

                return get_comments_by_post_id(query["post_id"])
        else:
            return get_comment_by_id(id), OK
    
    @login_required
    def post(current_user, self):
        errors = body_parser.validate(request.json)
        if errors:
            abort(400, str(errors))
        
        body = body_parser.load(request.json)

        return create_comment(body), OK

    @adm_required
    def put(current_user, self):
        errors = body_parser.validate(request.json)
        if errors:
            abort(400, str(errors))

        body = body_parser.load(request.json)

        return update_comment(body), OK

    @adm_required
    def delete(current_user, self, id = None):
        if id == None:
            abort(400, "Id must be provided for this kind of operation.")

        return delete_comment(id), OK
