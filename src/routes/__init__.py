from .users import users_bp
from .sockets import sokets_bp, register_socketio_events
from .conexion import conexion_bp

def init_app(app, socketio):
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(conexion_bp, url_prefix='/conexion')
    socketio.init_app(app)
