import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    SECRET_JWT_KEY = os.getenv("SECRET_JWT_KEY", "wedding")

    # Login duration in seconds
    LOGIN_TOKEN_DURATION = 21600

    ALLOWED_EXTENSIONS = [ 'png', 'jpg', 'jpeg' ]
    UPLOAD_FOLDER = "/usr/src/app/static/uploads"
    BASE_HOST = "http://localhost:5000"
