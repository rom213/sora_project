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
from datetime import datetime
from twilio.rest import Client


home_bp = Blueprint('home', __name__)

# cliente de twlio
account_sid = 'AC9ce167842853d1b6f468b62470161035'
auth_token = 'd3b1ee20624ffdeb7ee45b3a3314cd0a'

# Inicializa el cliente de Twilio
client = Client(account_sid, auth_token)


@home_bp.route('/upload_image', methods=['POST'])
def upload_img():
    if 'photo' not in request.files or 'RFID-Code' not in request.form:
        return jsonify({'message': 'Missing image file or RFID code'}), 404

    image_file = request.files['photo']
    card_code = request.form.get('RFID-Code')
    is_success = request.form.get('isSuccess')

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
            new_image = Register(image_path=filename, rfid_code=card_code,is_success=is_success )
            db.session.add(new_image)
            db.session.commit()

            return jsonify({'message': 'Image uploaded successfully'}), 200
        except Exception as e:
            return jsonify({'message': f'Error saving image: {e}'}), 500

    return jsonify({'message': 'Missing image file or RFID code'}), 404


@home_bp.route('all_register', methods=['GET'])
def all_register():
    register = []
    data = Register.query.all()
    for regis in data:
        formatted_date = regis.created_at.strftime('%Y-%m-%d %H:%M:%S')  # Formato: Año-Mes-Día Hora:Minutos:Segundos
        register.append({
            'rfid': regis.rfid_code,
            'image_path': regis.image_path,
            'is_success':regis.is_success,
            'created_at': formatted_date
        })
    return register



@home_bp.route('call_alarm', methods=['GET'])
def call_alarm():
    try:
        # Número de teléfono de Twilio (desde el cual se realiza la llamada)
        from_ = '+12193368792'

        # Número de teléfono al que deseas llamar
        to = '+573224668364'

        # URL del archivo TwiML que define lo que sucede durante la llamada
        url = 'http://demo.twilio.com/docs/voice.xml'

        # Realiza la llamada
        call = client.calls.create(
            to=to,
            from_=from_,
            url=url
        )
        return jsonify({'message': 'the call it was posible'}), 200
    except:
        return jsonify({'message': 'the call it wasnt posible'}), 200


    


