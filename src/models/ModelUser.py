from .entities.User import User
from .entities.Conexion import Conexion
from .entities.Message import Message
from sqlalchemy import asc, desc
from . import db
from flask_login import current_user
from sqlalchemy import desc

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
    def allPsychologyUsers(cls, user_id, rol):
        try:
            if rol == 'psi':
                conexions = Conexion.query.filter(Conexion.user_id == user_id or Conexion.user_id2 == user_id).all()
                result = []

                for conexion in conexions:
                    countMessage=0
                    mesagges_tem = Message.query.filter(Message.conexion_id == conexion.id).order_by(asc(Message.id)).all()
                    user = {}

                    if conexion.user_id != user_id:
                        user = User.query.filter(User.id == conexion.user_id).first()

                    mesagges = []
                    fullname = user.name + ' ' + user.lastname
                    
                    # Si no hay mensajes, añade la conexión en su lugar
                    if mesagges_tem:
                        for message in mesagges_tem:
                            mesagges.append({
                                'id': message.id,
                                'message': message.message,
                                'user_id': message.user_id,
                                'conexion_id': message.conexion_id,
                                'letters': user.init_letters()
                            })
                            if message.user_id !=user_id and message.readmessage==0:
                                countMessage=countMessage+1
                    
                    print(countMessage)
 
                    
                    result.append({
                        'id': user.id,
                        'username': user.username,
                        'conexion_id': conexion.id,
                        'fullname': fullname,
                        'name': user.name,
                        'lastname': user.lastname,
                        'userLoginId': user_id,
                        'rol': user.rol,
                        'color': user.color,
                        'letter': user.init_letters(),
                        'messages': mesagges,
                        'countMessage':countMessage
                    })
                
                # Ordenar por el último mensaje o conexión
                result.sort(
                    key=lambda x: max((msg['id'] if msg['id'] is not None else -1) for msg in x['messages']) if x['messages'] else -1,
                    reverse=True
                )         
                return result
            

            if rol == 'user':
                all_users = User.query.filter_by(rol='psi').all()
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
                    countMessage=0

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
                            if message.user_id !=user_id and message.readmessage==0:
                                countMessage=countMessage+1
                        
                    conexion_id = conexion.id if conexion else None
                    print(countMessage)
                    result.append({
                        'id': user.id,
                        'username': user.username,
                        'conexion_id': conexion_id,
                        'fullname': fullname,
                        'name': user.name,
                        'lastname': user.lastname,
                        'userLoginId': user_id,
                        'rol': user.rol,
                        'color': user.color,
                        'letter': letters,
                        'messages': mesagges,
                        'countMessage':countMessage
                    })
                
                result.sort(
                    key=lambda x: max((msg['id'] if msg['id'] is not None else -1) for msg in x['messages']) if x['messages'] else -1,
                    reverse=True
                )                
            
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