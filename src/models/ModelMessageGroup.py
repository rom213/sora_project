from .entities.User import User
from .entities.Group_message import Group_message
from datetime import datetime
from . import db

class ModelMessageGroup:
    @classmethod
    def all(cls):
        try:
            messages = db.session.query(Group_message, User).join(User, Group_message.user_id == User.id).all()
            return messages
        except Exception as exc:
            raise Exception(exc)
        
    @classmethod
    def update(cls, message_id, new_message):
        try:
            Group_message = db.session.query(Group_message).filter_by(id=message_id).first()
            if Group_message:
                Group_message.message = new_message
                Group_message.update_at = datetime.utcnow
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
                return True;
            
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
    
