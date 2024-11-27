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
            found_user = User.query.filter_by(username=user.username).first()
            
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
    def get_by_id(cls, id):
        try:
            user_tem=User.query.get(id)

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