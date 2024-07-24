from .. import db

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entidad = db.Column(db.String(10), unique=True, nullable=False)
    descripcion = db.Column(db.String(50), nullable=False)

    def __init__(self, descripcion):
        self.descripcion = descripcion
        self.entidad = self.generate_entidad()

    @staticmethod
    def generate_entidad():
        last_section = Section.query.order_by(Section.id.desc()).first()
        if last_section is None:
            return "A01"

        last_entidad = last_section.entidad
        letters = last_entidad[:-2]
        number = int(last_entidad[-2:])

        if number < 99:
            number += 1
            return f"{letters}{number:02}"
        else:
            new_letters = increment_letters(letters)
            return f"{new_letters}01"

def increment_letters(letters):
    # Function to increment the alphabetic part of entidad
    if not letters:
        return "A"
    letters_list = list(letters)
    for i in reversed(range(len(letters_list))):
        if letters_list[i] == 'Z':
            letters_list[i] = 'A'
        else:
            letters_list[i] = chr(ord(letters_list[i]) + 1)
            break
    else:
        letters_list.append('A')
    return ''.join(letters_list)
