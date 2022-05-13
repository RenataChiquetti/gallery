from flask.cli import FlaskGroup

from wedding import app, db
from werkzeug.security import generate_password_hash


cli = FlaskGroup(app)

from wedding.model.user import User

# This is for hard reset of database when start
# Should not run on production environment
@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()

    admin = User("admin", generate_password_hash("admin"), True)
    deleted = User("deleted", generate_password_hash("deleted"), False)
    db.session.add_all([admin, deleted])

    db.session.commit()


if __name__ == "__main__":
    cli()
