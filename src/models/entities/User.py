import random
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from config import Config
from extensions import get_serializer, bcrypt
from flask import current_app
from itsdangerous import (
    URLSafeTimedSerializer as Serializer,
    SignatureExpired,
    BadSignature,
)
from .. import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    rol = db.Column(db.String(20), nullable=True)
    name = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(40), nullable=False)
    color = db.Column(db.String(7), nullable=False, default="#FFFFFF")
    iuud = db.Column(db.String(16), nullable=False, default="0000000000000000")
    anonymous_user = db.Column(db.String(20), nullable=False)
    avatar = db.Column(db.String(100), nullable=True)
    group_messages = db.relationship("Group_message", backref="user", lazy=True)
    email = db.Column(db.String(120), unique=True, nullable=True)

    def __init__(
        self,
        username,
        password,
        email="",
        name="",
        lastname="",
        avatar="",
        anonymous_user="",
    ):
        self.username = username
        self.password = password
        self.name = name
        self.rol = "user"
        self.lastname = lastname
        self.color = self.generate_pastel_color()
        self.iuud = self.generate_user_id()
        self.avatar = avatar
        self.anonymous_user = anonymous_user
        self.email = email

    def generate_user_id(self):
        code = f"{random.randint(0, 999999999999999):015d}"
        return code

    serializer = Serializer(Config.SECRET_KEY)

    def generate_pastel_color(self):
        red = (random.randint(0, 255) + 255) // 2
        green = (random.randint(0, 255) + 255) // 2
        blue = (random.randint(0, 255) + 255) // 2
        return "#{:02x}{:02x}{:02x}".format(red, green, blue)

    def get_token(self):
        serializer = get_serializer()
        return serializer.dumps(
            {"user_id": self.id}, salt=current_app.config["SECURITY_PASSWORD_SALT"]
        )

    @classmethod
    def verify_token(cls, token, expiration=3600):
        serializer = get_serializer()
        try:
            data = serializer.loads(
                token,
                salt=current_app.config["SECURITY_PASSWORD_SALT"],
                max_age=expiration,
            )
        except SignatureExpired:
            return None, "Token Expirado"  # Devuelve None y el mensaje "Token Expirado"
        except BadSignature:
            return None, "Token Inválido"  # Devuelve None y el mensaje "Token Inválido"

        user = data.get("user_id")  # Extrae el user_id del token
        user = cls.query.get(user)  # Busca el usuario por ID en la base de datos
        
        if not user:
            return None, "Usuario no encontrado"  # Si el usuario no existe, devuelve el error
        
        return user, None  # Devuelve el objeto user y None si no hay error

    @classmethod
    def check_password(cls, hashed_password, password):
        return check_password_hash(hashed_password, password)


    @classmethod
    def get_by_id(cls, id):
        try:
            user = cls.query.get(id)
            if not user:
                raise ValueError(f"User with id {id} not found")
            return user
        except Exception as exc:
            raise Exception(f"Error retrieving user: {exc}")

    def __repr__(self):
        return f"<User {self.username}, Email: {self.email}>"

    def first_letter(self):
        return self.name[0].upper() if self.name else None

    def first_letter_of_lastname(self):
        return self.lastname[0].upper() if self.lastname else None

    def init_letters(self):
        first = self.first_letter()
        last = self.first_letter_of_lastname()
        return f"{first}{last}" if first and last else None

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "rol": self.rol,
            "name": self.name,
            "lastname": self.lastname,
            "color": self.color,
            "iuud": self.iuud,
            "messages":[],
            "anonymous_user": self.anonymous_user,
            "avatar": self.avatar,
            "letter":self.init_letters(),
            "fullname":self.name + ' ' + self.lastname
        }

