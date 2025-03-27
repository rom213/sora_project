import os


class Config:
    SECRET_KEY = 'laila'
    SECURITY_PASSWORD_SALT = 'perra'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'chatunity7@gmail.com'
    MAIL_PASSWORD = 'vncl refb besy tadl'
    MAIL_DEFAULT_SENDER = 'chatunity7@gmail.com'


class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = "localhost"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "roma"
    MYSQL_DB = "home"
    SQLALCHEMY_DATABASE_URI = "sqlite:///sora_project.db"

    # Aquí defines la carpeta de subida para los avatares
    UPLOAD_FOLDER = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "static/uploads"
    )


config = {"development": DevelopmentConfig}


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
