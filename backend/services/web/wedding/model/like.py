from . import db, ma


class Like(db.Model):
    __tablename__ = "likes"

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable = False)


class LikeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        include_fk = True
        model = Like
        load_instance = True

like_schema = LikeSchema()
like_schema_many = LikeSchema(many = True)
