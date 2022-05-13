from .. import db
from flask import abort

from werkzeug.security import generate_password_hash

from ..model.user import User, user_schema, user_schema_many
from ..model.like import Like
from ..model.comment import Comment
from ..model.post import Post

def create_user(user_data):

    query = User.query.filter_by(name = user_data["name"])

    if len(query.all()):
        abort(400, "Username already exists.")

    try:
        # Apply encryption
        user_data["password"] = generate_password_hash(user_data["password"])

        user = User(**user_data)
        
        db.session.add(user)
        db.session.commit()

        return user_schema.dump(user)
    except:
        abort(500, "Failed to create new user.")


def update_user(user_data):
    query = User.query.filter_by(id = user_data["id"])

    try:
        user = query.first()

        if user == None:
            raise
    except:
        abort(404, "Cannot find user with provided id.")

    try:
        rows = query.update(user_data)
        db.session.commit()

        if not rows:
            raise

        return user_schema.dump(query.first())
    except:
        abort(500, "Failed to update user.")


def delete_user(id):
    # Query to find target user
    query = User.query.filter_by(id = id)

    user = None
    try:
        # Get a copy of user to return for frontend
        user = query.first()

        if user == None:
            raise
    except:
        abort(404, "Cannot find user with provided id.")

    try:
        like_remove_query = Like.query.filter_by(user_id = user.id)
        match = like_remove_query.all()

        if len(match) > 0:
            like_remove_query.delete()
            db.session.commit()
    except:
        abort(500, "Failed to delete cascates.")

    try:
        comment_remove_query = Comment.query.filter_by(user_id = user.id)
        match = comment_remove_query.all()

        if len(match) > 0:
            comment_remove_query.delete()
            db.session.commit()
    except:
        abort(500, "Failed to delete cascates.")

    try:
        deleted = User.query.filter_by(name = "deleted").first()

        Post.query.filter_by(user_id = user.id).update({
            "user_id": deleted.id
        })
    except:
        abort(500, "Failed to delete cascates.")

    try:
        # Deletes the user from db
        dump_user = user_schema.dump(user)

        query.delete()
        db.session.commit()

        return dump_user
    except:
        abort(500, "Failed to delete user.")


def get_all_users():
    try:
        users = User.query.all()

        return user_schema_many.dump(users)
    except:
        abort(500, "Failed to query users.")


def get_user_by_id(id):
    try:
        user = User.query.filter_by(id = id).first()

        if user == None:
            raise

        return user_schema.dump(user)
    except:
        abort(404, "Cannot find user with provided id.")

def get_user_by_name(name):
    query = User.query.filter_by(name = name)

    try:
        user = query.first()

        if user == None:
            raise

        return user_schema.dump(user)
    except:
        abort(404, "Cannot find specifyed user.")
