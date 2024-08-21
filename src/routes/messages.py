from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy.exc import SQLAlchemyError
from flask_login import login_required
from models.ModelMessage import ModelMessage

from models import db


messages_bp = Blueprint('messages', __name__)

@messages_bp.route('/toato', methods=['POST'])
@login_required
def toato():
    if request.method == 'POST':
        conexion_id = request.form.get('conexion_id')

        if not conexion_id:
             flash('No connection ID provided.', 'error')
             return redirect(url_for('index'))

        try:
            ModelMessage.toato(conexion_id=conexion_id)
            flash('Interaction successful!', 'success')
            return redirect(url_for('index'))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f'Error on Iteration:{str(e)}', 'error')
            return render_template('index.html')

    return render_template('index.html')


@messages_bp.route('/all', methods=['GET'])
@login_required
def all():
    try:
            ModelMessage.all()
            return render_template('index.html')
    
    except SQLAlchemyError as e:
        flash(f'Error Retrieving message {str(e)}', 'error')
        return render_template('index.html')
    
    

@messages_bp.route('/delete', methods=['POST'])
@login_required
def delete():
       if request.method == 'POST':
        message_id = request.form.get('id')   

        if not message_id:
            flash('No message ID provided.', 'error')
            return redirect(url_for('index'))

        try:
                
            ModelMessage.delete(message_id=message_id)
            flash('Message deleted successfully')
            return redirect(url_for('index'))
            
        except SQLAlchemyError as e:

            db.session.rollback()
            flash(f'Error deleting message {str(e)}', 'error')
            return redirect(url_for('index'))
   



@messages_bp.route('/update', methods=['POST'])
@login_required
def update():
        
        if request.method == 'POST':
            message_id = request.form['id']
            new_message = request.form['message']

            if not new_message:
                flash('Message cannot be empty.', 'error')
                return redirect(url_for('update', id=message_id))
        
        try:
            ModelMessage.update(message_id=message_id, new_message= new_message)
            flash('Message updated successfully')
            return redirect(url_for('index'))
        
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f'Error updating message {str(e)}', 'error')
            return render_template('index.html')

  

