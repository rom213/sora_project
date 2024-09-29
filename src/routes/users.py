from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from flask_login import login_user, logout_user, login_required
from models.ModelUser import ModelUser, User
from models.entities.User import User
from models import db
from forms import ResetRequestForm, ResetPasswordForm
from extensions import mail, bcrypt
from flask_mail import Message
import os
from flask_login import current_user

from config import config, allowed_file

from flask_socketio import SocketIO, emit

# Selecciona la configuración de desarrollo
app_config = config["development"]

users_bp = Blueprint("users", __name__)


@users_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Obtener los datos del formulario
        username = request.form.get("username")
        password = request.form.get("password")
        name = request.form.get("name")
        lastname = request.form.get("lastname")
        anonymous_user = request.form.get("anonymous_user")
        avatar = request.files.get("avatar")
        email = request.form.get("email")

        # Validación del avatar (si hay)
        avatar_filename = None
        if avatar and avatar.filename != "":
            if allowed_file(avatar.filename):
                avatar_filename = save_avatar(avatar)
            else:
                flash("Invalid file type. Only .png, .jpg, .jpeg, .gif are allowed.")
                return render_template("auth/register.html")

        # Crear el objeto User
        user = User(
            username=username,
            password=generate_password_hash(password),  
            email = email,
            name=name,
            lastname=lastname,
            avatar=avatar_filename,
            anonymous_user=anonymous_user,
            is_verified=False  # El usuario no está verificado hasta que confirme el email
        )

        try:
            # Registrar el usuario en la base de datos
            ModelUser.register(user=user)
            
            # Enviar correo de verificación
            send_verification_email(user)
            
            # Mostrar mensaje para que el usuario verifique su correo
            flash("User created successfully! Please check your email to verify your account.", "success")
            return redirect(url_for("users.login"))

        except Exception as e:
            # Si ocurre un error, revertir la transacción
            db.session.rollback()
            flash(f"Error creating user: {str(e)}", "danger")
            
            # Eliminar el avatar si se había subido
            if avatar_filename:
                delete_avatar(avatar_filename)
            return render_template("auth/register.html")

    # Mostrar el formulario de registro
    return render_template("auth/register.html")



@users_bp.route('/update', methods=['GET','POST'])
@login_required
def update():
    if request.method == 'POST':
        name = request.form.get('name')
        lastname = request.form.get('lastname')
        anonymous_user=request.form.get('anonymous_user')
        avatar = request.files.get('avatar')


        user =ModelUser.get_by_id(current_user.id);

        avatar_filename = None
        if avatar and avatar.filename != '':
            if allowed_file(avatar.filename):
                avatar_filename = save_avatar(avatar)

        if avatar_filename:
            user.avatar=avatar_filename
        user.name=name
        user.lastname=lastname
        user.anonymous_user=anonymous_user

        try:
            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating user: {str(e)}')
            if avatar_filename:
                delete_avatar(avatar_filename)
            return render_template('auth/register.html')

    return render_template('auth/register.html')

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User(username=username, password=password)
        logged_user = ModelUser.login(user)

        if logged_user and logged_user.password:
            if logged_user.is_verified:
                login_user(logged_user)
                return redirect(url_for("index"))
            else:
                flash("Please verify your account before logging in.", "warning")
                return render_template("auth/login.html")
        else:
            flash("Invalid username or password")
            return render_template("auth/login.html")

    return render_template("auth/login.html")


@users_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("users.login"))


@users_bp.route("/home")
@login_required
def home():
    return render_template("home.html")




@users_bp.route('/<int:iuud>', methods=['GET'])
@login_required
def getUserIuud(iuud):
    data = ModelUser.get_by_iuud(iuud=iuud)
    if data:
        return jsonify(data.to_dict())
    else:
        return jsonify({"error": "Usuario no encontrado"}), 404



@users_bp.route('/admin', methods=['GET', 'POST'])
@login_required
def getUsersForAdmin():
    if request.method == 'GET':
        data_tem= ModelUser.get_users_by_admin()
        if data_tem:
            data=[]
            for user in data_tem:
                data.append(user.to_dict())
            return jsonify(data), 200
        else:
            return jsonify({"error": "Usuarios no encontrado"}), 404

    if request.method == 'POST':
        data = request.json
        rol=data.get('rol')
        user_id=data.get('user_id')
        data= ModelUser.updateRolUser(rol=rol, user_id=user_id)
        
        if data:
            userLogin = {
                "id": data.id,
                "username": data.username,
                "rol": data.rol,
                "name": data.name,
                "lastname": data.lastname,
                "color": data.color,
                "avatar": data.avatar,
                "letters":data.init_letters()
            }

            emit('user_data', userLogin, broadcast=True, namespace='/')
            return jsonify({"error": "rol actualizado"}), 201
        else:
            return jsonify({"error": "user not found"}), 404       

    


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


def send_email(user):
    token = user.get_token()
    reset_url = url_for("users.reset_token", token=token, _external=True)
    msg = Message(
        "Password Reset Request", recipients=[user.email], sender="MAIL_USERNAME"
    )
    
    msg.body = f"""To reset your password, please follow the link below:{reset_url}

            If you didn't request a password reset, please ignore this email."""

    # Enviar el correo
    mail.send(msg)


@users_bp.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    form = ResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_email(user)
            flash("Reset request sent. Check your Email.", "success")
        
        else:
             flash("Email address not found. Please check and try again.", "danger")
        return redirect(url_for("users.login"))
    return render_template(
        "Reset_request/reset_request.html",
        title=("Reset Request"),
        form=form,
        legend=("Reset request"),
    )


@users_bp.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    user, error = User.verify_token(token)
    if error:
        pass
    else:
        pass

    if user is None:
        flash("That is invalid or expired. Please try again.", "warning")
        return redirect(url_for("users.reset_request"))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  # Hash de la nueva contraseña
        user.password = hashed_password  # Establece el nuevo hash de la contraseña
        db.session.commit()
        flash("Password changed! Please login")
        return redirect(url_for("users.login"))

    return render_template(
        "Reset_password/reset_password.html",
        title="Change Password",
        legend="Change Password",
        form=form
    )


def send_verification_email(user):
    token = user.get_token()  
    verification_url = url_for('users.verify_email', token=token, _external=True)

    msg = Message("Verify your account", recipients=[user.email], sender=current_app.config['MAIL_DEFAULT_SENDER'])
    msg.body = f'''Welcome to our platform,

Please verify your account by clicking the following link:
{verification_url}

If you did not create this account, please ignore this email.
'''

    mail.send(msg)



@users_bp.route('/verify_email/<token>')
def verify_email(token):
    user, error = User.verify_token(token)
    if user:
        user.is_verified = True  
        db.session.commit()
        flash("Your account has been verified. You can now log in.", "success")
        return redirect(url_for('users.login'))
    else:
        flash("The verification link is invalid or has expired: {error}", "danger")
        return redirect(url_for('users.register'))
