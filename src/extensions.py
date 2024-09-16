# extensions.py
from flask_socketio import SocketIO
from flask_mysqldb import MySQL
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask import current_app
from itsdangerous import URLSafeTimedSerializer
from flask_bcrypt import Bcrypt

# Crear instancias de las extensiones
db = SQLAlchemy()

bcrypt = Bcrypt()
mysql = MySQL()
login_manager_app = LoginManager()
mail = Mail()
socketio = SocketIO(cors_allowed_origins="*")

def get_serializer():
    return URLSafeTimedSerializer(
        secret_key=current_app.config['SECRET_KEY'],
        salt=current_app.config['SECURITY_PASSWORD_SALT']
    )