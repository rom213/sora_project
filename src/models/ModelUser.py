from .entities.User import User
from .entities.Conexion import Conexion
from .entities.Message import Message
from sqlalchemy import asc, desc
from . import db
from flask_login import current_user

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
            user_id = current_user.id
            result = []
            for user in all_users:
                letters = user.first_letter() + user.first_letter_of_lastname()
                fullname = user.name + ' ' + user.lastname

                conexion = db.session.query(Conexion).filter(
                    Conexion.user_id2 == user.id,
                    Conexion.user_id == user_id
                ).first()

                mesagges_tem = []
                mesagges = []

                if conexion:
                    mesagges_tem = db.session.query(Message).filter(Message.conexion_id == conexion.id).order_by(asc(Message.id)).all()

                    for message in mesagges_tem:

                        mesagges.append({
                            'id': message.id,
                            'message': message.message,
                            'user_id': message.user_id,
                            'conexion_id': message.conexion_id,
                            'letters': letters
                        })

                conexion_id = conexion.id if conexion else None

                result.append({
                    'id': user.id,
                    'username': user.username,
                    'conexion_id': conexion_id,
                    'fullname': fullname,
                    'name': user.name,
                    'lastname': user.lastname,
                    'userLoginId': current_user.id,
                    'rol': user.rol,
                    'color': user.color,
                    'letter': letters,
                    'messages': mesagges
                })
            return result

        except Exception as exc:
            raise Exception(exc) 
        

    @classmethod
    def get_by_id(cls, id):
        try:
            user_tem=User.query.get(id)

            return user_tem
        except Exception as exc:
            raise Exception(exc)