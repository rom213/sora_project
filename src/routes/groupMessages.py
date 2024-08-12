from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from flask_login import login_user, logout_user, login_required
from models.ModelMessageGroup import ModelMessageGroup
from models.entities.Group_message import Group_message
from models import db


group_messages_bp = Blueprint('group_messages', __name__)

@group_messages_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        user_id = request.form['user_id']
        message = request.form['message']

        group_messages = Group_message(message=message, user_id=user_id)

        # Añadir el nuevo usuario a la base de datos
        try:
            ModelMessageGroup.create(group_message=group_messages)
            flash('Message created successfully!')
            return redirect(url_for('users.login'))
        except Exception as e:
            db.session.rollback()
            flash('Error creating Message')
            return render_template('auth/register.html')

    return render_template('auth/register.html')


@group_messages_bp.route('/all', methods=['GET', 'POST'])
def all():
    
    if request.method == 'POST':

        Group_message = User(username=request.form['username'], password=request.form['password'])
        logged_user = ModelUser.login(user)

        if logged_user is not None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('index'))
            else:
                flash("password_invalid...")
                return render_template('auth/login.html')
        else:
            flash("user not found...")
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

@users_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users.login'))

@users_bp.route('/home')
@login_required
def home():
    return render_template('home.html')
