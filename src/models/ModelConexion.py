from .entities.Conexion import Conexion
from sqlalchemy.exc import SQLAlchemyError
from flask_login import current_user

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
    def create(cls, user_id2):
        try:
            user_id= current_user.id
            conexion = Conexion(user_id2=user_id2, user_id=user_id)
            db.session.add(conexion)
            db.session.commit()

            return conexion

        except Exception as exc:
            raise Exception(exc)
        
    @classmethod
    def delete(cls, id_conexion):
        try:
            conexion=Conexion.query.filter_by(id=id_conexion).first()
            if not conexion:
                raise Exception("Connection record not found")
            
            db.session.delete(conexion)
            db.session.commit()
            return True;
        except SQLAlchemyError as exc:
            db.session.rollback()  # Rollback the session in case of an error
            raise Exception(f"Database error: {exc}")
        except Exception as exc:
            raise Exception(f"Error: {exc}")
        