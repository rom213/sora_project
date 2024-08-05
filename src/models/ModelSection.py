from .entities.Section import Section
from .entities.Slot import Slot
from . import db

class ModelSection:
    @classmethod
    def allSections(cls):
        try:
            allSections = Section.query.options(db.joinedload(Section.slots)).all()
            print(allSections)
            return allSections;
        except Exception as exc:
            raise Exception(exc)
        
    @classmethod
    def create(cls,description):
        try:
            section= Section(descripcion=description)
            db.session.add(section)
            db.session.commit()
        except Exception as exc:
            raise Exception(exc)