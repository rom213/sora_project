from .entities.User import User
from .entities.Group_message import Group_message
from datetime import datetime
from sqlalchemy import asc, desc
from . import db

class ModelMessageGroup:
    @classmethod
    def all(cls):
        try:
            # Asumiendo que `Group_message` tiene los campos `id`, `content`, y `user_id`
            messages = db.session.query(Group_message, User).join(User, Group_message.user_id == User.id).order_by(asc(Group_message.created_at)).all()
            
            # Convertir los resultados en un formato de lista de diccionarios
            result = []
            for message, user in messages:
                result.append({
                    'id': message.id,
                    'message': message.message,
                    'username': user.username,  # Suponiendo que User tiene un campo `username`
                    'name': user.name,
                    'user_id': user.id,
                    'rol':user.rol
                })
            return result
        except Exception as exc:
            raise Exception(exc)
        
    @classmethod
    def update(cls, message_id, new_message):
        try:
            Group_messages = db.session.query(Group_message).filter_by(id=message_id).first()
            if Group_messages:
                Group_messages.message = new_message
                Group_messages.update_at = datetime.utcnow()
                db.session.commit()
                return True
            
            return False
        except Exception as exc:
            raise Exception(exc)
        



    @classmethod
    def create(cls, group_message):
        try:
            if Group_message:
                db.session.add(group_message);
                db.session.commit();
                data=ModelMessageGroup.all()
                return data;
            
            return False;
        except Exception as exc:
            raise Exception(exc)
    
    

        
    @classmethod
    def delete(cls, message_id):
        try:
            Group_message = db.session.query(Group_message).filter_by(id=message_id).first()

            if Group_message:
                db.session.delete(Group_message)
                db.session.commit()
                return True
            
            return False;
        except Exception as exc:
            raise Exception(exc)
    
