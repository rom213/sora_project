# app.py
from flask import Flask, render_template, redirect, url_for, jsonify


from config import config
from models import db  # Importa db desde models/__init__.py
from models.ModelUser import ModelUser
from routes import init_app, register_socketio_events
from models.ModelMessageGroup import ModelMessageGroup
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


@app.route("/")
def root():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    else:
        return redirect(url_for("users.login"))
    
@app.route("/messages")
@login_required
def messages():
    allPsy=ModelUser.allPsychologyUsers(user_id=current_user.id, rol= current_user.rol)
    toato=ModelUser.allUsersByToaTo(user_id=current_user.id)
    messages=ModelMessageGroup.all()
    userLogin = {
                "id": current_user.id,
                "username": current_user.username,
                "rol": current_user.rol,
                "name": current_user.name,
                "iuud": current_user.iuud,
                "lastname": current_user.lastname,
                "color": current_user.color,
                "avatar": current_user.avatar,
                "letters":current_user.init_letters(),
                "anonymous_user":current_user.anonymous_user
            }
    
    data={
        'messages':messages,
        'psychology':allPsy,
        'userLogin':userLogin,
        'toato':toato
    }

    return jsonify(data), 200



@app.route("/index")
@login_required
def index():
    allPsy=ModelUser.allPsychologyUsers(user_id=current_user.id, rol= current_user.rol)
    toato=ModelUser.allUsersByToaTo(user_id=current_user.id)
    messages=ModelMessageGroup.all()
    userLogin = {
                "id": current_user.id,
                "username": current_user.username,
                "rol": current_user.rol,
                "name": current_user.name,
                "iuud": current_user.iuud,
                "lastname": current_user.lastname,
                "color": current_user.color,
                "avatar": current_user.avatar,
                "letters":current_user.init_letters(),
                "anonymous_user":current_user.anonymous_user
            }
    return render_template("index.html", messages=messages, psychology=allPsy, userLogin=userLogin, toato=toato)

# Inicializa Blueprints y eventos de SocketIO
init_app(app, socketio)
register_socketio_events(socketio)

if __name__ == "__main__":
    pass;
