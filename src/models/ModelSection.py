from .entities.Section import Section
from . import db

class ModelSection:
    @classmethod
    def allSections(cls):
        try:
            allSections = Section.query.all()
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