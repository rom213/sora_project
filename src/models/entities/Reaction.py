from datetime import datetime
from .. import db

class Reaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    raction = db.Column(db.String(100), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow, nullable=True)
    delete_at = db.Column(db.DateTime,  nullable=True)


    def __init__(self, reaction, user_id, state_id):
        self.state_id=state_id
        self.reaction = reaction
        self.user_id = user_id

