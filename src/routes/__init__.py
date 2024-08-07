from .users import users_bp
from .groupMessages import group_messages_bp
from .sockets import sokets_bp, register_socketio_events

def init_app(app, socketio):
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(group_messages_bp, url_prefix='/groupMessages')
    socketio.init_app(app)

    
