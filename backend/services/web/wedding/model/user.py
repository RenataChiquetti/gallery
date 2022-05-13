from . import db, ma
from datetime import datetime


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), unique = True, nullable = False)
    password = db.Column(db.String(200), unique = False, nullable = False)
    is_adm = db.Column(db.Boolean, default = False, nullable = False)
    created_on = db.Column(db.DateTime, default = datetime.now())

    posts = db.relationship("Post", backref = "user", lazy = True)
    comments = db.relationship("Comment", backref = "user", lazy = True)
    likes = db.relationship("Like", backref = "user", lazy = True)

    def __init__(self, name, password, is_adm):
        self.name = name
        self.password = password
        self.is_adm = is_adm


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True


user_schema = UserSchema()
user_schema_many = UserSchema(many = True)
