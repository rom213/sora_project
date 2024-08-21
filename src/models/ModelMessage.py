from .entities.User import User
from .entities.Conexion import Conexion
from .entities.Message import Message
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