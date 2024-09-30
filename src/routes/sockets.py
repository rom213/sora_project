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
            conexion_type=data.get('conexion_type')
            
            if not conexion_id:
                conexion = ModelConexion.create(user_id2=data.get('user_id'), conexion_type=conexion_type)
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

    @socketio.on('message_toato')
    def handle_message_toato(data):
        if current_user.is_authenticated:
            conexion_type=data.get('conexion_type')
            conexion_id = data.get('conexion_id')
            
            messages = new_func_message(data, conexion_type, conexion_id)

            if messages:
                first_user = messages[0]
                if current_user.id == first_user.get('userLoginId'):
                    emit('message_toato', messages, broadcast=True)
                    
                
                messages=ModelUser.allUsersByToaTo(user_id=data.get('user_id'))
                emit('message_toato', messages, broadcast=True)
        else:
            print("Anonymous user sent a message")
    


    @socketio.on('conexion_delete')
    def handle_delete_conexion(data):
        if current_user.is_authenticated:
            conexion_type=data.get('conexion_type')
            conexion_id = data.get('conexion_id')
            
            if conexion_id:
                ModelConexion.delete(id_conexion=conexion_id);
                if conexion_type=='toato':
                    messages=ModelUser.allUsersByToaTo(user_id=data.get('user_id'))
                    if not messages:
                        messages=[{
                            'userLoginId': data.get('user_id'),
                            'data':False
                        }]
                        
                    emit('message_toato', messages, broadcast=True)

                if conexion_type=='psi':
                    messages=ModelUser.allPsychologyUsers(user_id=data.get('user_id'), rol=data.get('rol'))
                    emit('message_psi', messages, broadcast=True)

                
        else:
            print("Anonymous user sent a message")


    @socketio.on('message_update')
    def message_update(data):
        if current_user.is_authenticated:
            action_type=data.get('action_type')
            message_id = data.get('message_id')
            user_id=data.get('user_id')
            messages_type=data.get('messages_type')
            message=data.get('message')

            if message_id:
                if messages_type=='group':
                    if action_type=='delete':
                       ModelMessageGroup.delete(message_id=message_id);
                    if action_type=='update':
                       ModelMessageGroup.update(message_id=message_id, new_message=message)
                    emit('message', ModelMessageGroup.all(), broadcast=True)

                if messages_type=='toato':
                    if action_type=='delete':
                        ModelMessage.delete(message_id=message_id);
                    if action_type=='update':
                        ModelMessage.update(message_id=message_id,new_message=message)


                    messages = ModelUser.allUsersByToaTo(user_id=current_user.id)
                    emit('message_toato', messages, broadcast=True)
                            
                        
                    messages=ModelUser.allUsersByToaTo(user_id=data.get('user_id'))
                    emit('message_toato', messages, broadcast=True)


                if messages_type=='psi':
                        if action_type=='delete':
                            ModelMessage.delete(message_id=message_id);
                        
                        if action_type=='update':
                            ModelMessage.update(message_id=message_id,new_message=message)



                        allPsychology = ModelUser.allPsychologyUsers(user_id=current_user.id, rol=current_user.rol)
                        emit('message_psi', allPsychology, broadcast=True)
                        
                        allPsychology=ModelUser.allPsychologyUsers(user_id=data.get('user_id'), rol=data.get('rol'))
                        emit('message_psi', allPsychology, broadcast=True)

        else:
            print("Anonymous user sent a message")




    def new_func_message(data, conexion_type, conexion_id):
        if not conexion_id: 
            conexion=ModelConexion.findConexion(user_id=data.get('user_id'), type_conexion=conexion_type);
            if conexion:
                conexion_id=conexion.id
            if not conexion:
                conexion = ModelConexion.create(user_id2=data.get('user_id'), conexion_type=conexion_type)
                if conexion:
                    conexion_id = conexion.id
        messages=ModelMessage.createToato(message=data.get('message'), conexion_id=conexion_id)
        return messages



    
    
    
    
    
    
    
    @socketio.on('read_message')
    def read_message(data):
        if current_user.is_authenticated:
            ModelMessage.readMessage(conexion_id=data.get('conexion_id'),user_id=data.get('user_id'))
        else:
            print("Anonymous user sent a message")


    
