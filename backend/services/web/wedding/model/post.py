from . import db, ma
from datetime import datetime


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key = True)
    allowed = db.Column(db.Boolean, default = False, nullable = False)
    path = db.Column(db.String, default="", nullable = False)
    created_on = db.Column(db.DateTime, default = datetime.now())

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)

    comments = db.relationship("Comment", backref = "post", lazy = True)
    likes = db.relationship("Like", backref = "post", lazy = True)

    def __init__(self, allowed, path):
        self.allowed = allowed
        self.path = path


class PostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        include_fk = True
        model = Post
        load_instance = True

post_schema = PostSchema()
post_schema_many = PostSchema(many = True)
