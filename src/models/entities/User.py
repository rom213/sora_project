from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .. import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    rol = db.Column(db.String(20), nullable=True)
    fullname = db.Column(db.String(100), nullable=True)

    def __init__(self, username, password, fullname=""):
        self.username = username
        self.password = password
        self.fullname = fullname

    @classmethod
    def check_password(cls, hashed_password, password):
        return check_password_hash(hashed_password, password)
    
    @classmethod
    def get_by_id(cls, id):
        try:
            user = cls.query.get(id)
            if not user:
                raise ValueError(f'User with id {id} not found')
            return user
        except Exception as exc:
            raise Exception(f'Error retrieving user: {exc}')

    def __repr__(self):
        return f'<User {self.username}>'
