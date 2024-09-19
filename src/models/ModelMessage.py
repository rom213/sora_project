from .entities.User import User
from .entities.Conexion import Conexion
from .entities.Message import Message
from .ModelUser import ModelUser

from flask_login import current_user

from . import db


class ModelMessage:
    @classmethod
    def toato(cls, conexion_id):
        try:
            messages = (
                db.session.query(Message)
                .filter(conexion_id==conexion_id)
                .all()
            )
            return messages
        except Exception as exc:
            raise Exception(exc)

    @classmethod
    def all(cls, conexion_id):
        try:
            messages = (
                db.session.query(Message, User)
                .join(User, Message.user_id == User.id)
                .join(Conexion, Message.conexion_id == Conexion.id)
                .filter(Message.conexion_id == conexion_id)
                .all()
            )
            return messages
        except Exception as exc:
            raise Exception(exc)

    @classmethod
    def delete(cls, message_id):
        try:
            delete = db.session.query(Message).filter_by(Message.id == message_id).first()
            
            if delete:
                db.session.delete(delete)
                db.session.commit()
                return True
            
            return False
        
        except Exception as exc:
            db.session.rollback()  
            raise Exception(f"Error deleting messages: {exc}")


    @classmethod
    def update(cls, message_id, new_message):
        try:
            edit = db.session.query(Message).filter_by(id == message_id).first()
            if edit:
                edit.message_id= new_message
                db.session.commit()
                return True
            
            return False
            
        except Exception as e:
            raise e
        
    @classmethod
    def readMessage(cls, conexion_id, user_id):
        try:
            # Actualiza directamente los mensajes que cumplen con los criterios
            updated_rows = db.session.query(Message).filter(
                Message.conexion_id == conexion_id,
                Message.user_id == user_id,
                Message.readmessage == 0
            ).update({Message.readmessage: 1})  # Cambia a True si prefieres booleano

            # Guarda los cambios en la base de datos
            db.session.commit()

            # Verifica si se actualizaron registros
            return updated_rows > 0

        except Exception as e:
            # Deshacer cualquier cambio en caso de error
            db.session.rollback()
            raise e

    @classmethod
    def create(cls, message, conexion_id):
        try:
            user_id = current_user.id

            message = Message(message=message, user_id=user_id, conexion_id=conexion_id)
            
            db.session.add(message)
            db.session.commit()
            
            return ModelUser.allPsychologyUsers(user_id, rol=current_user.rol)
            
        except Exception as e:
            raise e
        
    @classmethod
    def createToato(cls, message, conexion_id):
        try:
            user_id = current_user.id

            message = Message(message=message, user_id=user_id, conexion_id=conexion_id)
            
            db.session.add(message)
            db.session.commit()
            
            return ModelUser.allUsersByToaTo(user_id=user_id)
            
        except Exception as e:
            raise e