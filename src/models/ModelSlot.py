from .entities.Slot import Slot
from . import db

class ModelSlot:
    @classmethod
    def allSlots(cls):
        try:
            allSections = Slot.query.all()
            return allSections;
        except Exception as exc:
            raise Exception(exc)
        
    @classmethod
    def create(cls,car_id, section_id):
        try:
            section= Slot(car_id=car_id,section_id=section_id)
            db.session.add(section)
            db.session.commit()
        except Exception as exc:
            raise Exception(exc)
        
    @classmethod
    def delete(cls,slot_id):
        try:
            slot= db.session.query(Slot).filter_by(id=slot_id).one()
            db.session.delete(slot)
            db.session.commit()
        except Exception as exc:
            raise Exception(exc)