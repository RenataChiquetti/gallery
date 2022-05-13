import os
from flask import send_file, abort
from flask_restful import Resource

from ..utils.auth import login_required


UPLOAD_FOLDER = "/usr/src/app/static/uploads"


class ImageRoute(Resource):
    def get(self, file):
        try:
            img_dir = UPLOAD_FOLDER
            img_path = os.path.join(img_dir, file)
            return send_file(img_path, mimetype='image/*')
        except:
            abort(404, "Cannot find required image.")
