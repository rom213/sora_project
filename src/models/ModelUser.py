from .entities.User import User
from .entities.Conexion import Conexion
from .entities.Message import Message
from sqlalchemy import asc, desc
from . import db
from flask_login import current_user
from sqlalchemy import desc
from datetime import datetime
from sqlalchemy import or_, and_

class ModelUser:
    @classmethod
    def login(cls, user):
        try:
            found_user = User.query.filter_by(email=user.email).first()
            
            if found_user and User.check_password(found_user.password, user.password):
                return found_user
            else:
                return None
        except Exception as exc:
             raise Exception(f"Error in login: {str(exc)}")
        
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
    def allUsersByToaTo(cls, user_id):
        try:
            conexions = Conexion.query.filter(and_(and_(or_(Conexion.user_id == user_id, Conexion.user_id2 == user_id), Conexion.conexion_type == 'toato'), Conexion.delete_at==None)).all()
            
            result = []
            for conexion in conexions:
                    countMessage=0
                    mesagges_tem = Message.query.filter(Message.conexion_id == conexion.id).order_by(asc(Message.id)).all()
                    user = {}
                    if conexion.user_id2 != user_id:
                        user = User.query.filter(User.id == conexion.user_id2).first()
                    if conexion.user_id != user_id:
                        user = User.query.filter(User.id == conexion.user_id).first()

                    if conexion.user_id == user_id and conexion.user_id2==user_id:
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
                                'letters': user.init_letters(),
                                'avatar':user.avatar
                            })
                            if message.user_id !=user_id and message.readmessage==0:
                                countMessage=countMessage+1
                    result.append({
                        'id': user.id,
                        'username': user.username,
                        'conexion_id': conexion.id,
                        'fullname': fullname,
                        'name': user.name,
                        'lastname': user.lastname,
                        'userLoginId': user_id,
                        'rol': user.rol,
                        'avatar':user.avatar,
                        'color': user.color,
                        'letter': user.init_letters(),
                        'messages': mesagges,
                        'countMessage':countMessage,
                        'conexion_type': conexion.conexion_type,
                        'data':True
                    })
                
                    # Ordenar por el último mensaje o conexión
            result.sort(
                        key=lambda x: max((msg['id'] if msg['id'] is not None else -1) for msg in x['messages']) if x['messages'] else -1,
                        reverse=True
                    )         
            return result

        except Exception as exc:
            raise Exception(exc)
        
    @classmethod
    def allPsychologyUsers(cls, user_id, rol):
        try:
            if rol == 'psi':
                conexions = Conexion.query.filter(and_(and_(or_(Conexion.user_id == user_id, Conexion.user_id2 == user_id), Conexion.conexion_type=='psi'), Conexion.delete_at==None)).all()
                result = []

                for conexion in conexions:
                    countMessage=0
                    mesagges_tem = Message.query.filter(Message.conexion_id == conexion.id).order_by(asc(Message.id)).all()
                    user = {}

                    if conexion.user_id2 != user_id:
                        user = User.query.filter(User.id == conexion.user_id2).first()
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
                        'avatar':user.avatar,
                        'lastname': user.lastname,
                        'userLoginId': user_id,
                        'rol': user.rol,
                        'color': user.color,
                        'letter': user.init_letters(),
                        'messages': mesagges,
                        'countMessage':countMessage,
                        'anonymous_user':user.anonymous_user,
                        'conexion_type': conexion.conexion_type
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

                    conexion = db.session.query(Conexion).filter(and_(and_(Conexion.user_id2 == user.id, Conexion.user_id == user_id),
                    Conexion.delete_at==None)).first()

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
                    result.append({
                        'id': user.id,
                        'username': user.username,
                        'conexion_id': conexion_id,
                        'fullname': fullname,
                        'avatar':user.avatar,
                        'name': user.name,
                        'lastname': user.lastname,
                        'userLoginId': user_id,
                        'rol': user.rol,
                        'color': user.color,
                        'letter': letters,
                        'messages': mesagges,
                        'countMessage':countMessage,
                        'conexion_type': conexion.conexion_type if conexion else None
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
        
    
    @classmethod
    def get_by_iuud(cls, iuud):
        try:
            user_tem=User.query.filter(User.iuud== iuud).first()
            
            return user_tem
        except Exception as exc:
            raise Exception(exc)
        

    @classmethod
    def updateRolUser(cls, user_id, rol):
        try:
            user = db.session.query(User).filter_by(id=user_id).first()
            if user:
                user.rol = rol
                user.update_at = datetime.utcnow()
                db.session.commit()
                return user
            
            return False
        except Exception as exc:
            raise Exception(exc)
        
    @classmethod
    def get_users_by_admin(cls):
        try:
            users_tem = User.query.filter(or_(User.rol == 'psi', User.rol == 'admin')).all()
            
            return users_tem
        except Exception as exc:
            raise Exception(exc)