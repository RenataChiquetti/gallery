from .. import db
from flask import abort

from ..model.comment import Comment, comment_schema, comment_schema_many
from ..model.user import User
from ..model.post import Post

def create_comment(comment_data):
    user = None
    try:
        user = User.query.filter_by(id = comment_data["user_id"]).first()

        if user == None:
            raise
    except:
        abort(400, "Cannot find provided user_id for comment creation.")
    del comment_data["user_id"]

    post = None
    try:
        post = Post.query.filter_by(id = comment_data["post_id"]).first()

        if post == None:
            raise
    except:
        abort(400, "Cannot find provided post_id for comment creation.")
    del comment_data["post_id"]

    try:
        comment = Comment(**comment_data)
        comment.user = user
        comment.post = post

        db.session.add(comment)
        db.session.commit()

        return comment_schema.dump(comment)
    except:
        abort(500, "Failed to create new comment.")


def update_comment(comment_data):
    try:
        user = User.query.filter_by(id = comment_data["user_id"]).first()

        if user == None:
            raise
    except:
        abort(400, "Cannot find provided user_id for post creation.")

    try:
        post = Post.query.filter_by(id = comment_data["post_id"]).first()

        if post == None:
            raise
    except:
        abort(400, "Cannot find provided post_id for comment creation.")

    query = Comment.query.filter_by(id = comment_data["id"])
    try:
        comment = query.first()

        if comment == None:
            raise
    except:
        abort(404, "Cannot find comment with provided id.")

    try:
        rows = query.update(comment_data)
        db.session.commit()

        if not rows:
            raise

        return comment_schema.dump(query.first())
    except:
        abort(500, "Failed to update comment.")


def delete_comment(id):
    # Query to find target post
    query = Comment.query.filter_by(id = id)

    comment = None
    try:
        # Get a copy of post to return for frontend
        comment = query.first()

        if comment == None:
            raise
    except:
        abort(404, "Cannot find comment with provided id.")

    try:
        # Deletes the post from db
        query.delete()
        db.session.commit()

        return comment_schema.dump(comment)
    except:
        abort(500, "Failed to delete comment.")


def get_all_comments():
    try:
        comments = Comment.query.all()

        dumped_comments = []
        for comment in comments:
            dump = comment_schema.dump(comment)
            dump["name"] = comment.user.name
            dumped_comments.append(dump)

        return dumped_comments
    except:
        abort(500, "Failed to query comment.")


def get_comment_by_id(id):
    try:
        comment = Comment.query.filter_by(id = id).first()

        if comment == None:
            raise

        dumped_comment = comment_schema.dump(comment)
        dumped_comment["name"] = comment.user.name

        return dumped_comment
    except:
        abort(404, "Cannot find comment with provided id.")

def get_comments_by_post_id(post_id):
    query = Comment.query.filter_by(post_id = post_id)

    try:
        comments = query.all()

        dumped_comments = []
        for comment in comments:
            dump = comment_schema.dump(comment)
            dump["name"] = comment.user.name
            dumped_comments.append(dump)

        return dumped_comments
    except:
        abort(500, "Failed to query comments by post_id.")
