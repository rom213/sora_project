from flask import Flask, render_template
from flask_socketio import SocketIO, send
from config import config
from models import db  # Importa db desde models/__init__.py
from flask_mysqldb import MySQL
from flask_login import LoginManager
from models.ModelUser import ModelUser
from routes import init_app, register_socketio_events

app = Flask(__name__)
app.config.from_object(config['development'])

# Inicializa extensiones
db.init_app(app)
mysql = MySQL(app)
login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(id)

socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template("index.html")

# Inicializa Blueprints y eventos de SocketIO
init_app(app, socketio)
register_socketio_events(socketio)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crea las tablas si no existen
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)
