
from lib2to3.pgen2 import token
import jwt
from .. import app
from functools import wraps
from datetime import datetime, timedelta
from flask import jsonify, request
from werkzeug.security import check_password_hash

from ..service.user import get_user_by_name


def auth(name, password):
    if not name or not password:
        return "Could not verify authorization values.", 401

    user = None
    try:
        user = get_user_by_name(name)
    except:
        return "Could not find username.", 401

    if user and check_password_hash(user["password"], password):
        expiration = datetime.now() + timedelta(seconds = app.config["LOGIN_TOKEN_DURATION"])

        token = jwt.encode({'name': user["name"], 'exp': expiration }, app.config["SECRET_JWT_KEY"])

        return jsonify({ "token": token, "exp": expiration })

    return "Authorization failed.", 401


def check_auth():
    token = request.headers.get("Authorization")

    if not token:
        return "Missing authorization token.", 401
    try:
        data = jwt.decode(token, app.config['SECRET_JWT_KEY'], algorithms=['HS256'])

        current_user = get_user_by_name(data['name'])
    except:
        return "Invalid or expired token.", 401
    
    return jsonify(current_user)


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return "Missing authorization token.", 401
        try:
            data = jwt.decode(token, app.config['SECRET_JWT_KEY'], algorithms=['HS256'])

            # Its best pratice cache this operation but here
            # I focused on simplicity, in real production env
            # a cache in memory would be better to reduce db stress
            current_user = get_user_by_name(data['name'])
        except:
            return "Invalid or expired token.", 401
        return f(current_user, *args, **kwargs)
    return decorated


def adm_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return "Missing authorization token.", 401
        try:
            data = jwt.decode(token, app.config['SECRET_JWT_KEY'], algorithms=['HS256'])

            # Its best pratice cache this operation but here
            # I focused on simplicity, in real production env
            # a cache in memory would be better to reduce db stress
            current_user = get_user_by_name(data['name'])

            if not current_user["is_adm"]:
                return "You must be admin to perform this operation.", 403 
        except:
            return "Invalid or expired token.", 401
        return f(current_user, *args, **kwargs)
    return decorated
