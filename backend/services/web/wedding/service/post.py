from .. import db
from flask import abort

from ..model.post import Post, post_schema, post_schema_many
from ..model.user import User

def create_post(post_data):
    user = None
    try:
        user = User.query.filter_by(id = post_data["user_id"]).first()

        if user == None:
            raise
    except:
        abort(400, "Cannot find provided user_id for post creation.")
    del post_data["user_id"]

    try:
        post = Post(**post_data)
        post.user = user

        db.session.add(post)
        db.session.commit()

        return post_schema.dump(post)
    except:
        abort(500, "Failed to create new post.")


def update_post(post_data):
    try:
        user = User.query.filter_by(id = post_data["user_id"]).first()

        if user == None:
            raise
    except:
        abort(400, "Cannot find provided user_id for post creation.")

    query = Post.query.filter_by(id = post_data["id"])
    try:
        post = query.first()

        if post == None:
            raise
    except:
        abort(404, "Cannot find post with provided id.")

    try:
        rows = query.update(post_data)
        db.session.commit()

        if not rows:
            raise

        return post_schema.dump(query.first())
    except:
        abort(500, "Failed to update post.")


def delete_post(id):
    # Query to find target post
    query = Post.query.filter_by(id = id)

    post = None
    try:
        # Get a copy of post to return for frontend
        post = query.first()

        if post == None:
            raise
    except:
        abort(404, "Cannot find post with provided id.")

    try:
        # Deletes the post from db
        query.delete()
        db.session.commit()

        return post_schema.dump(post)
    except:
        abort(500, "Failed to delete post.")


def get_allowed_posts():
    try:
        posts = Post.query.filter_by(allowed = True).all()

        dumped_posts = []
        for post in posts:
            dump = post_schema.dump(post)
            dump["name"] = post.user.name
            dumped_posts.append(dump)

        return dumped_posts
    except:
        abort(500, "Failed to query post.")


def get_all_posts():
    try:
        posts = Post.query.all()

        dumped_posts = []
        for post in posts:
            dump = post_schema.dump(post)
            dump["name"] = post.user.name
            dumped_posts.append(dump)

        return dumped_posts
    except:
        abort(500, "Failed to query post.")


def get_post_by_id(id):
    try:
        post = Post.query.filter_by(id = id).first()

        if post == None:
            raise

        dumped_post = post_schema.dump(post)
        dumped_post["name"] = post.user.name

        return dumped_post
    except:
        abort(404, "Cannot find post with provided id.")
