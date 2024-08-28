from .entities.User import User
from . import db

class ModelUser:
    @classmethod
    def login(cls, user):
        try:
            found_user = User.query.filter_by(username=user.username).first()
            if found_user and User.check_password(found_user.password, user.password):
                return found_user
            else:
                return None
        except Exception as exc:
            raise Exception(exc)
        
    @classmethod
    def register(cls, user):
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as exc:
            raise Exception(exc)
        
    @classmethod
    def allUsers(cls):
        try:
            allUsers = User.query.all()
            return allUsers;
        except Exception as exc:
            raise Exception(exc)
        
    @classmethod
    def allPsychologyUsers(cls):
        try:
            all_users = User.query.filter_by(rol='psi').all()
            result = []
            for user in all_users:
                result.append({
                    'id': user.id,
                    'username': user.username,
                    'fullname': user.fullname,
                    'user_id': user.id,
                    'rol':user.rol,
                    'color':user.color
                })
            return result

        except Exception as exc:
            raise Exception(exc)
        
        
    @classmethod
    def get_by_id(cls, id):
        try:
            return User.query.get(id)
        except Exception as exc:
            raise Exception(exc)