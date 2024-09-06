from flask import Flask, render_template, redirect, url_for
from flask_socketio import SocketIO, send
from config import config
from models import db  # Importa db desde models/__init__.py
from flask_mysqldb import MySQL
from flask_login import LoginManager, current_user, login_required
from models.ModelUser import ModelUser
from routes import init_app, register_socketio_events
from models.ModelMessageGroup import ModelMessageGroup
from models.ModelUser import ModelUser
from models.entities.Group_message import Group_message


from flask_login import current_user


app = Flask(__name__)
app.config.from_object(config['development'])

# Inicializa extensiones
db.init_app(app)
mysql = MySQL(app)
login_manager_app = LoginManager(app)
login_manager_app.login_view = 'users.login'



@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(id)

socketio = SocketIO(app, cors_allowed_origins="*")



@app.route('/')
def root():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    else:
        return redirect(url_for('users.login'))

@app.route('/index')
@login_required
def index():
    allPsy=ModelUser.allPsychologyUsers(user_id=current_user.id, rol= current_user.rol)
    messages=ModelMessageGroup.all()
    userLogin = {
                "id": current_user.id,
                "username": current_user.username,
                "rol": current_user.rol,
                "name": current_user.name,
                "lastname": current_user.lastname,
                "color": current_user.color,
                "avatar": current_user.avatar,
                "letters":current_user.init_letters()
            }
    return render_template("index.html", messages=messages, psychology=allPsy, userLogin=userLogin)

# Inicializa Blueprints y eventos de SocketIO
init_app(app, socketio)
register_socketio_events(socketio)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crea las tablas si no existen
    socketio.run(app, host='0.0.0.0', port=5006, debug=True)
