from .entities.User import User
from .entities.Group_message import Group_message
from datetime import datetime
from sqlalchemy import asc, desc
from . import db

class ModelMessageGroup:
    @classmethod
    def all(cls):
        try:
            
            messages = db.session.query(Group_message, User).join(User, Group_message.user_id == User.id).order_by(asc(Group_message.created_at)).all()
            
            result = []

            for message, user in messages:
                
                letters= user.first_letter() + user.first_letter_of_lastname()

                result.append({
                    'id': message.id,
                    'message': message.message,
                    'username': user.username,
                    'name': user.name,
                    'avatar':user.avatar,
                    'user_id': user.id,
                    'rol':user.rol,
                    'avatar':user.avatar,
                    'letters':letters,
                    'color':user.color
                })
            return result
        except Exception as exc:
            raise Exception(exc)
        
    @classmethod
    def update(cls, message_id, new_message):
        try:
            group_messages = Group_message.query.filter(Group_message.id==message_id).first()
            print(group_messages)
            if group_messages:
                group_messages.message = new_message
                group_messages.update_at = datetime.utcnow()
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
            group_message = Group_message.query.filter(Group_message.id==message_id).first()

            if group_message:
                db.session.delete(group_message)
                db.session.commit()
                return True
            
            return False;
        except Exception as exc:
            raise Exception(exc)
    
