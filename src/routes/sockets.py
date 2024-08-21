from flask import Blueprint, request, jsonify
from flask_socketio import SocketIO, emit
from models.entities.Group_message import Group_message
from models.ModelMessageGroup import ModelMessageGroup
from flask_login import current_user

sokets_bp = Blueprint('sokets', __name__)

# Definir socketio globalmente
socketio = None

def register_socketio_events(socketio_instance):
    global socketio
    socketio = socketio_instance

    @socketio.on('message')
    def handle_message(message):
        if current_user.is_authenticated:
            user_id = current_user.id
            group_messages = Group_message(message=message, user_id=user_id)
            messages=ModelMessageGroup.create(group_message=group_messages)
            if message != "User connected!":
                emit('message', messages, broadcast=True)
        else:
            print("Anonymous user sent a message")
