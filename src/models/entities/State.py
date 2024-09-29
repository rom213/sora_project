from datetime import datetime
from .. import db

class State(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    image = db.Column(db.String(100), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow, nullable=True)
    delete_at = db.Column(db.DateTime,  nullable=True)


    def __init__(self, title, user_id, image):
        self.image=image
        self.title = title
        self.user_id = user_id

