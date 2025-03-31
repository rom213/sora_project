from flask import Blueprint, request, jsonify
from flask_socketio import SocketIO, emit
import requests
from websocket import create_connection, WebSocket
import threading
import json
import logging



sokets_bp = Blueprint('sokets', __name__)

buttons_state = {
    'security': False,
    'opendoor': False,
    'offlights': False,
    'signal_close_door':False,
    'alarm': False,
    'room': False,
    'dinning': False,
    'bathroom': False,
    'yarn': False,
    'closeDoor':True,
    'ethernet': False,
    'ethernet_state':False
}


@sokets_bp.route('/checkDoor', methods=['POST'])
def checkDoor():
    buttons_state["closeDoor"] = request.json.get("closeDoor")
    emit_status_update();
    return jsonify({'message': 'funciona'}), 200



NODE_SERVER_URL = "http://localhost:5000/update_buttons"
NODE_SERVER_WS_URL = "ws://localhost:5000"

# Definir socketio globalmente
socketio = None
status_ethernet=False
ws = None

@sokets_bp.route('/update_buttons', methods=['POST'])
def update_buttons():
    global buttons_state
    buttons_state = request.json

    emit_status_update()
    return jsonify(buttons_state), 200

@sokets_bp.route('/check_ethernet', methods=['POST'])
def esp32_isconected():
    if not request.json.get("online"):
        buttons_state["ethernet"] = False

    buttons_state["ethernet_state"] = request.json.get("online")

    emit_status_update()
    return jsonify(request.json), 200






def emit_status_update():
    global socketio
    if socketio:
        print(buttons_state);
        socketio.emit('status_update', buttons_state, namespace='/')

def register_socketio_events(socketio_instance):
    global socketio
    socketio = socketio_instance

    @socketio.on('connect')
    def handle_connect():
        emit('status_update', buttons_state)

    @socketio.on('toggle_button')
    def handle_toggle_button(data):
        button = data['button']
        buttons_state[button] = not buttons_state[button]
        emit('status_update', buttons_state, broadcast=True)
        # Notify the Node.js server about the button state change
        requests.post(NODE_SERVER_URL, json=buttons_state)
        # Also send update via WebSocket
        if ws:
            ws.send(json.dumps(buttons_state))

    @socketio.on('temperature')
    def handle_temperature(temperature):
        print("received temperature= " + str(temperature))

        emit('temperature_flask', str(temperature),broadcast=True)

        
    

    @socketio.on('message')
    def handle_message(message):
        print("received message= " + message)
        if message != "User connected!":
            emit('message', message, broadcast=True)

            
def send_ws_update():
    global ws
    try:
        if ws and ws.connected:
            logging.debug("Sending data through WebSocket")
            ws.send(json.dumps(buttons_state))
        else:
            logging.warning("WebSocket is closed. Reconnecting...")
            connect_ws()
            ws.send(json.dumps(buttons_state))
    except WebSocket.ConnectionClosedException as e:
        logging.error(f"Failed to send data: {e}")
        connect_ws()

def connect_ws():
    global ws
    try:
        ws = create_connection(NODE_SERVER_WS_URL)
        logging.info("WebSocket connection established")
    except Exception as e:
        logging.error(f"Failed to connect WebSocket: {e}")

def start_ws_client():
    global ws
    while True:
        try:
            connect_ws()
            while ws.connected:
                result = ws.recv()
                if result:
                    data = json.loads(result)
                    logging.debug(f"Received data from WebSocket: {data}")
                    global buttons_state
                    buttons_state = data
                    emit_status_update()
        except WebSocket.ConnectionClosed:
            logging.warning("WebSocket connection closed, reconnecting...")
            continue
        except Exception as e:
            logging.error(f"WebSocket error: {e}")
            continue

# Run WebSocket client in a separate thread
ws_thread = threading.Thread(target=start_ws_client)
ws_thread.start()