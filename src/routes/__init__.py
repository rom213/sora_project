from .users import users_bp
from .sockets import sokets_bp, register_socketio_events

def init_app(app, socketio):
    app.register_blueprint(users_bp, url_prefix='/users')
    socketio.init_app(app)
