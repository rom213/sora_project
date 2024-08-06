from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from flask_login import login_user, logout_user, login_required
from models.ModelUser import ModelUser
from models.entities.User import User
from models import db

users_bp = Blueprint('users', __name__)

@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        fullname = request.form['fullname']

        user = User(username=username, password=generate_password_hash(password), fullname=fullname)

        # Añadir el nuevo usuario a la base de datos
        try:
            db.session.add(user)
            db.session.commit()
            flash('User created successfully!')
            return redirect(url_for('users.login'))
        except Exception as e:
            db.session.rollback()
            flash('Error creating user')
            return render_template('auth/register.html')

    return render_template('auth/register.html')

@users_bp.route('/register/dashboard', methods=['POST'])
def registerDashboard():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        fullname = request.form['fullname']

        user = User(username=username, password=generate_password_hash(password), fullname=fullname)

        # Añadir el nuevo usuario a la base de datos
        try:
            db.session.add(user)
            db.session.commit()
            flash('User created successfully!')
            return redirect(url_for('users.login'))
        except Exception as e:
            db.session.rollback()
            flash('Error creating user')
            return redirect(url_for('users.register'))


@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User(username=request.form['username'], password=request.form['password'])
        logged_user = ModelUser.login(user)

        if logged_user is not None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('dashboard.dashboard'))
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
