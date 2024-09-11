from flask import Blueprint, request, jsonify
from flask_socketio import SocketIO, emit
from models.entities.Group_message import Group_message
from models.ModelMessageGroup import ModelMessageGroup
from models.ModelMessage import ModelMessage
from models.ModelConexion import ModelConexion
from models.ModelUser import ModelUser

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

    @socketio.on('message_psi')
    def handle_message_psi(data):
        if current_user.is_authenticated:
            conexion_id = data.get('conexion_id')
            
            if not conexion_id:
                conexion = ModelConexion.create(user_id2=data.get('user_id'))
                if conexion:
                    conexion_id = conexion.id

            group_messages = ModelMessage.create(message=data.get('message'), conexion_id=conexion_id)

            if group_messages:
                first_user = group_messages[0]
                if current_user.id == first_user.get('userLoginId'):
                    allPsychology = ModelUser.allPsychologyUsers(user_id=current_user.id, rol=current_user.rol)

                    emit('message_psi', allPsychology, broadcast=True)
                    
                
                allPsychology=ModelUser.allPsychologyUsers(user_id=data.get('user_id'), rol=data.get('rol'))
                emit('message_psi', allPsychology, broadcast=True)
        else:
            print("Anonymous user sent a message")

    @socketio.on('read_message')
    def read_message(data):
        if current_user.is_authenticated:
            ModelMessage.readMessage(conexion_id=data.get('conexion_id'),user_id=data.get('user_id'))
        else:
            print("Anonymous user sent a message")


    
