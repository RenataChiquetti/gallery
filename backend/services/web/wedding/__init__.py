from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from .model import db, ma

# Creates flask app instance
app = Flask(__name__)
# Set the config object
app.config.from_object("wedding.config.Config")

CORS(app, resources = { r"/*": { "origins": "*" } })

# Import of models for SQLalchemy correct working
from .model.like import Like, LikeSchema
from .model.comment import Comment, CommentSchema
from .model.post import Post, PostSchema
from .model.user import User, UserSchema

# Init the instance with current app
db.init_app(app)

# Init the instance with current app
ma.init_app(app)

from .api.user import UserRoute
from .api.post import PostRoute
from .api.like import LikeRoute
from .api.login import LoginRoute
from .api.image import ImageRoute
from .api.comment import CommentsRoute

# Creates an api instance from flask restful
api = Api(app)

# Configures the api routing
api.add_resource(LoginRoute, "/login")
api.add_resource(UserRoute, "/user", "/user/<int:id>")
api.add_resource(LikeRoute, "/like", "/like/<int:post_id>", "/like/user/<int:like_post_id>")
api.add_resource(CommentsRoute, "/comment", "/comment/<int:id>")
api.add_resource(PostRoute, "/post", "/post/<int:id>")
api.add_resource(ImageRoute, "/image/<string:file>")
