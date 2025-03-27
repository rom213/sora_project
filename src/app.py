# app.py
from flask import Flask, render_template, redirect, url_for, jsonify




from config import config
from models import db  # Importa db desde models/__init__.py
from models.ModelUser import ModelUser
from routes import init_app, register_socketio_events
from flask_login import current_user, login_required
from extensions import (
    mysql,
    login_manager_app,
    mail,
    socketio,
    bcrypt,
)

app = Flask(__name__)
app.config.from_object(config["development"])


db.init_app(app)
mysql.init_app(app)
login_manager_app.init_app(app)
mail.init_app(app)
bcrypt.init_app(app)
login_manager_app.login_view = "users.login"




@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(id)

@app.route("/index")
@login_required
def index():
    return render_template('dashboard/body/body.html')



@app.route("/")
def root():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    else:
        return redirect(url_for("users.login"))
    



# Inicializa Blueprints y eventos de SocketIO
init_app(app, socketio)
register_socketio_events(socketio)

if __name__ == "__main__":
    pass;
