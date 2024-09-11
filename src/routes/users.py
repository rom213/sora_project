from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from flask_login import login_user, logout_user, login_required
from models.ModelUser import ModelUser
from models.entities.User import User
from models import db
import os
from config import config, allowed_file

# Selecciona la configuración de desarrollo
app_config = config['development']

users_bp = Blueprint('users', __name__)

@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        name = request.form.get('name')
        lastname = request.form.get('lastname')
        anonymous_user=request.form.get('anonymous_user')
        avatar = request.files.get('avatar')

        avatar_filename = None
        if avatar and avatar.filename != '':
            if allowed_file(avatar.filename):
                avatar_filename = save_avatar(avatar)
            else:
                flash("Invalid file type. Only .png, .jpg, .jpeg, .gif are allowed.")
                return render_template('auth/register.html')

        user = User(username=username, password=generate_password_hash(password), name=name, lastname=lastname, avatar=avatar_filename,anonymous_user=anonymous_user) 


        try:
            ModelUser.register(user=user)
            flash('User created successfully!')
            return redirect(url_for('users.login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating user: {str(e)}')
            if avatar_filename:
                delete_avatar(avatar_filename)
            return render_template('auth/register.html')

    return render_template('auth/register.html')

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User(username=username, password=password)
        logged_user = ModelUser.login(user)

        if logged_user and logged_user.password:
            login_user(logged_user)
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password")
            return render_template('auth/login.html')

    return render_template('auth/login.html')

@users_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users.login'))

@users_bp.route('/home')
@login_required
def home():
    return render_template('home.html')



@users_bp.route('/<int:iuud>', methods=['GET'])
def getUserIuud(iuud):
    data= ModelUser.get_by_iuud(iuud=iuud)
    if data:
         return jsonify(data.to_dict())
    else:
        return jsonify({"error": "Usuario no encontrado"}), 404  

    




def save_avatar(avatar):
    """Guardar el archivo de avatar en la carpeta designada."""
    avatar_filename = secure_filename(avatar.filename)
    avatar_path = os.path.join(app_config.UPLOAD_FOLDER, avatar_filename)
    os.makedirs(app_config.UPLOAD_FOLDER, exist_ok=True)
    avatar.save(avatar_path)
    return avatar_filename

def delete_avatar(filename):
    """Eliminar el archivo de avatar si ocurre un error al crear el usuario."""
    avatar_path = os.path.join(app_config.UPLOAD_FOLDER, filename)
    if os.path.exists(avatar_path):
        os.remove(avatar_path)
