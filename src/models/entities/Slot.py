from .. import db

class Slot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, unique=True, nullable=True)
    section_id = db.Column(db.String(10), db.ForeignKey('section.entidad'), nullable=False)

    def __init__(self, section_id, car_id=None):
        self.section_id = section_id
        self.car_id = car_id