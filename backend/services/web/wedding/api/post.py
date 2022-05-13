import os
import uuid
from http.client import OK
from flask import request, abort
from flask_restful import Resource
from marshmallow import Schema, fields
from werkzeug.utils import secure_filename
from .. import app

from ..utils.auth import adm_required, login_required

from ..service.post import create_post, delete_post, get_all_posts, get_allowed_posts, get_post_by_id, update_post

# For url parameters validation
class PostQuerySchema(Schema):
    allowed = fields.Int(required = True, help = "allowed is a required field")

# For comment body parsing
class PostBodySchema(Schema):
    id = fields.Int(required = False, help = "Identification of the post")
    allowed = fields.Bool(required = True, help = "allowed must be provided")
    path = fields.Str(required = True, help = "path must be provided")
    user_id = fields.Int(required = True, help = "user_id must be provided")


# Parser instances
body_parser = PostBodySchema()
query_parser = PostQuerySchema()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

class PostRoute(Resource):
    @login_required
    def get(current_user, self, id = None):
        if not current_user["is_adm"]:
            return get_allowed_posts(), OK

        errors = query_parser.validate(request.args)

        if id == None and (not errors):
            return get_allowed_posts(), OK
        elif id == None and (errors):
            return get_all_posts(), OK
        else:
            return get_post_by_id(id), OK
    
    @login_required
    def post(current_user, self):

        if "file" not in request.files:
            abort(400, "You must provide a file for this operation")

        file = request.files["file"]

        if file.filename == '':
            abort(400, "No selected file")

        filename = None
        if file and allowed_file(file.filename):
            filename = secure_filename(str(uuid.uuid4().hex) + "." + file.filename.rsplit('.', 1)[1].lower())
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        return create_post({
            "allowed": False,
            "path": app.config["BASE_HOST"] + "/image/" + filename,
            "user_id": current_user["id"]
        }), OK


    @adm_required
    def put(current_user, self):
        errors = body_parser.validate(request.json)
        if errors:
            abort(400, str(errors))
        
        body = body_parser.load(request.json)

        return update_post(body), OK

    @adm_required
    def delete(current_user, self, id = None):
        if id == None:
            abort(400, "Id must be provided for this kind of operation.")

        return delete_post(id), OK
