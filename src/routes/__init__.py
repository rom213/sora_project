from .users import users_bp
from .dashboard import dashboard_bp
from .sections import section_bp
from .slots import slot_bp
from .home import home_bp

def init_app(app):
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(section_bp, url_prefix='/sections')
    app.register_blueprint(slot_bp, url_prefix='/slots')
    app.register_blueprint(home_bp, url_prefix='/home')
