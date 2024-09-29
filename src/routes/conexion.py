from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.ModelConexion import ModelConexion
from flask_login import current_user, login_required

conexion_bp = Blueprint('conexion', __name__)

@conexion_bp.route('/all', methods=['POST'])
@login_required
def all():
    if request.method == 'POST':
        user_id = current_user.id
        conexions=ModelConexion.all(id_user=user_id);
        return render_template('index.html', conexions=conexions)

@conexion_bp.route('/delete', methods=['POST'])
def delete():
    if request.method == 'POST':
        id_conexion = request.form['id_conexion']
        ModelConexion.delete(id_conexion=id_conexion)

        return redirect(url_for('conexion.all'))
