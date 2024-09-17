from .entities.Conexion import Conexion
from sqlalchemy.exc import SQLAlchemyError
from flask_login import current_user
from sqlalchemy import or_, and_
from datetime import datetime

from . import db

class ModelConexion:
    @classmethod
    def all(cls, id_user):
        try:
            all_conexion_users = Conexion.query.filter_by(user_id=id_user).all()
            return all_conexion_users if all_conexion_users else None
        except Exception as exc:
            raise Exception(exc)
        
    @classmethod
    def findConexion(cls, user_id, type_conexion):
        try:
            user_id_loggout=current_user.id

            conexion_user = Conexion.query.filter(and_(or_(and_(Conexion.user_id==user_id_loggout, Conexion.user_id2==user_id),and_(Conexion.user_id==user_id, Conexion.user_id2==user_id_loggout)), Conexion.conexion_type==type_conexion, Conexion.delete_at==None)).first()


            return conexion_user if conexion_user else None
        except Exception as exc:
            raise Exception(exc)
        
    @classmethod
    def create(cls, user_id2, conexion_type):
        try:
            user_id= current_user.id
            conexion = Conexion(user_id2=user_id2, user_id=user_id, conexion_type=conexion_type)
            db.session.add(conexion)
            db.session.commit()

            return conexion

        except Exception as exc:
            raise Exception(exc)
        
    @classmethod
    def delete(cls, id_conexion):
        try:
            conexion=Conexion.query.filter(Conexion.id==id_conexion).first()
            if not conexion:
                raise Exception("Connection record not found")
            conexion.delete_at=datetime.utcnow()

            db.session.commit()
            return True;
        except SQLAlchemyError as exc:
            db.session.rollback()  # Rollback the session in case of an error
            raise Exception(f"Database error: {exc}")
        except Exception as exc:
            raise Exception(f"Error: {exc}")
        