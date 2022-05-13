from . import db, ma
from datetime import datetime

class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.Text, default = "", nullable = False)
    created_on = db.Column(db.DateTime, default = datetime.now())
    
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))

    def __init__(self, content):
        self.content = content


class CommentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        include_fk = True
        model = Comment
        load_instance = True

comment_schema = CommentSchema()
comment_schema_many = CommentSchema(many = True)
