from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from flask_login import login_user, logout_user, login_required
from models.ModelMessageGroup import ModelMessageGroup
from models.entities.Group_message import Group_message
from models import db


group_messages_bp = Blueprint('group_messages', __name__)

@group_messages_bp.route('/create', methods=['POST'])
@login_required
def create():
    if request.method == 'POST':
        user_id = request.form['user_id']
        message = request.form['message']

        group_messages = Group_message(message=message, user_id=user_id)

        # Añadir el nuevo usuario a la base de datos
        try:
            ModelMessageGroup.create(group_message=group_messages)
            flash('Message created successfully!')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash('Error creating Message')
            return render_template('index.html')

    return render_template('index.html')


@group_messages_bp.route('/all', methods=['GET'])
@login_required
def all():
    try:
            ModelMessageGroup.all()
            return render_template('index.html')
    
    except Exception as e:
        flash('Error Retrieving message')
        return render_template('index.html')
    
    

@group_messages_bp.route('/delete', methods=['POST'])
@login_required
def delete():
       if request.method == 'POST':
        id = request.form['id']     

        # Eliminar el mensaje de la base de datos
        try:
                
            ModelMessageGroup.delete(message_id=id)
            flash('Message deleted successfully')
            
        except Exception as e:

            db.session.rollback()
            flash('Error deleting message')
            return redirect(url_for('index'))
   



@group_messages_bp.route('/update', methods=['POST'])
@login_required
def update():
        
        if request.method == 'POST':
            id = request.form['id']
            new_message = request.form['message']
        
        # Actualizar el mensaje en la base de datos
        try:
            ModelMessageGroup.update(message_id=id, new_message= new_message)
            flash('Message updated successfully')
            return redirect(url_for('index'))
        
        except Exception as e:
            db.session.rollback()
            flash('Error updating message')
            return render_template('index.html')

  

