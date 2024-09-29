from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
from flask_login import login_user, logout_user, login_required
from models.ModelState import ModelState
from models import db
import os
from flask_login import current_user

from config import config, allowed_file

from flask_socketio import SocketIO, emit

# Selecciona la configuración de desarrollo
app_config = config["development"]

states_bp = Blueprint("states", __name__)


@states_bp.route("/save", methods=["GET", "POST"])
def save():
    if request.method == "POST":
        if 'image' not in request.files:
            return jsonify({"error": "No se encontró una imagen"}), 400
        
        if 'title' not in request.form:
            return jsonify({"error": "No se encontró un title"}), 400
        
        image = request.files['image']
        title = request.form['title']
        

        filepath = None
        if image and image.filename != "":
            if allowed_file(image.filename):
                filepath = save_state(image)
        if filepath:
            ModelState.create(path_img=filepath,title=title)
            emit('update_states', [], broadcast=True, namespace='/')
            return jsonify({"imagen": "imagen guardada"}), 200

        

        return jsonify({"imagen": "imagen no guardada"}), 403
    

@states_bp.route("/all", methods=["GET"])
def all():
    user_log = current_user.id
    states = ModelState.allStates(user_log=user_log)
    
    if states:
        return jsonify(states), 200  # Retorna un 200 OK si todo es correcto
    else:
        return jsonify({"error": "No states found"}), 404

        



def save_state(avatar):
    """Guardar el archivo de avatar en la carpeta designada."""
    avatar_filename = secure_filename(avatar.filename)
    avatar_path = os.path.join(app_config.UPLOAD_FOLDER, avatar_filename)
    os.makedirs(app_config.UPLOAD_FOLDER, exist_ok=True)
    avatar.save(avatar_path)
    return avatar_filename


def delete_state(filename):
    """Eliminar el archivo de avatar si ocurre un error al crear el usuario."""
    avatar_path = os.path.join(app_config.UPLOAD_FOLDER, filename)
    if os.path.exists(avatar_path):
        os.remove(avatar_path)