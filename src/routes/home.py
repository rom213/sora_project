import os
from models.entities.Register import Register, db
import uuid  # Para generar UUID
import hashlib  # Para crear un hash de la imagen
from flask import Blueprint, jsonify, request, current_app
from datetime import datetime
from PIL import Image
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from io import BytesIO

home_bp = Blueprint('home', __name__)



@home_bp.route('/upload_image', methods=['POST'])
def upload_img():
    if 'photo' not in request.files or 'RFID-Code' not in request.form:
        return jsonify({'message': 'Missing image file or RFID code'}), 404

    image_file = request.files['photo']
    card_code = request.form.get('RFID-Code')

    if image_file and card_code:
        upload_folder = current_app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        try:
            # Leer la imagen directamente desde el archivo
            image = Image.open(BytesIO(image_file.read()))
            
            # Generar un hash único de la imagen
            image_file.seek(0)  # Reiniciar el puntero del archivo
            image_hash = hashlib.md5(image_file.read()).hexdigest()  # MD5 hash
            
            # Crear un nombre de archivo único usando UUID y el hash
            unique_id = uuid.uuid4().hex  # Generar un UUID
            filename = secure_filename(f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{unique_id}_{image_hash[:8]}.jpg")
            filepath = os.path.join(upload_folder, filename)
            
            # Guardar la imagen en formato jpg
            image.save(filepath, 'JPEG')

            # Guardar la imagen en la base de datos
            new_image = Register(image_path=filepath, rfid_code=card_code)
            db.session.add(new_image)
            db.session.commit()

            return jsonify({'message': 'Image uploaded successfully'}), 200
        except Exception as e:
            return jsonify({'message': f'Error saving image: {e}'}), 500

    return jsonify({'message': 'Missing image file or RFID code'}), 404


