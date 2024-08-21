from datetime import datetime
from .. import db

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(256), nullable=False)
    conexion_id = db.Column(db.Integer, db.ForeignKey('conexion.id'), nullable=False)    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    

    def __init__(self, message, user_id, conexion_id):
        self.message = message
        self.user_id = user_id
        self.conexion_id = conexion_id

