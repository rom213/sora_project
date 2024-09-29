from .users import users_bp
from .groupMessages import group_messages_bp
from .messages import messages_bp
from .sockets import sokets_bp, register_socketio_events
from .conexion import conexion_bp
from .states import states_bp

def init_app(app, socketio):
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(conexion_bp, url_prefix='/conexion')
    app.register_blueprint(group_messages_bp, url_prefix='/groupMessages')
    app.register_blueprint(messages_bp, url_prefix='/messages')
    app.register_blueprint(states_bp, url_prefix='/states')
    socketio.init_app(app)

    
