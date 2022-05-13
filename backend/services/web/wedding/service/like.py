from .. import db
from flask import abort

from ..model.like import Like
from ..model.user import User
from ..model.post import Post

def like(user_id, post_id):
    like = None
    try:
        query = Like.query.filter_by(user_id = user_id, post_id = post_id)
        like = query.first()

        if like == None:
            user = User.query.filter_by(id = user_id).first()
            post = Post.query.filter_by(id = post_id).first()

            like = Like()
            like.user = user
            like.post = post
            db.session.add(like)
            db.session.commit()
        else:
            query.delete()
            db.session.commit()
    except:
        abort(500, "Failed to alter like.")


def check_like(user_id, post_id):
    like = None
    try:
        query = Like.query.filter_by(user_id = user_id).filter_by(post_id = post_id)
        like = query.first()

        if like == None:
            return False
        else:
            return True
    except:
        abort(500, "Failed to check like.")


def check_like_by_post(post_id):
    try:
        query = Like.query.filter_by(post_id = post_id)
        likes = query.all()

        return len(likes)
    except:
        abort(500, "Failed to count like.")
