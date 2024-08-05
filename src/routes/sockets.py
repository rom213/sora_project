from flask import Blueprint, request, jsonify
from flask_socketio import SocketIO, emit

sokets_bp = Blueprint('sokets', __name__)


# Definir socketio globalmente
socketio = None

def register_socketio_events(socketio_instance):
    global socketio
    socketio = socketio_instance

    @socketio.on('message')
    def handle_message(message):
        print("received message= " + message)
        if message != "User connected!":
            emit('message', message, broadcast=True)
