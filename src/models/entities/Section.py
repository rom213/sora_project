from .. import db

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entidad = db.Column(db.String(10), unique=True, nullable=False)
    descripcion = db.Column(db.String(50), nullable=False)
    slots = db.relationship('Slot', backref='section', lazy=True)

    def __init__(self, descripcion):
        self.descripcion = descripcion
        self.entidad = self.generate_entidad()

    def generate_entidad(self):
        last_section = Section.query.order_by(Section.id.desc()).first()
        
        if last_section:
            last_entidad = last_section.entidad
            return self.next_entidad(last_entidad)
        else:
            return 'A'
    
    def next_entidad(self, current):
        if not current:
            return 'A'
        
        last_char = current[-1]
        if last_char != 'Z':
            return current[:-1] + chr(ord(last_char) + 1)
        else:
            if len(current) == 1:
                return 'AA'
            else:
                return self.next_entidad(current[:-1]) + 'A'