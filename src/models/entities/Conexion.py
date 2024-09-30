from .. import db
from datetime import datetime

class Conexion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_id2 = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    conexion_type=db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow, nullable=True)
    delete_at = db.Column(db.DateTime,  nullable=True)

    def __init__(self, user_id, user_id2, conexion_type):
        self.user_id = user_id
        self.user_id2 = user_id2
        self.conexion_type=conexion_type