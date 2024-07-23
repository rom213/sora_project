from flask import Flask, redirect, url_for
from models.ModelUser import ModelUser
from config import config
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_mysqldb import MySQL
from flask_cors import CORS
from routes import init_app as init_routes




app = Flask(__name__)
CORS(app)

app.config.from_object(config['development'])

db = MySQL(app)
login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)

# Registrar los blueprints
init_routes(app)

@app.route('/')
def index():
    return redirect(url_for('users.login'))

# Manejo de errores
@app.errorhandler(401)
def status_401(error):
    return redirect(url_for('users.login'))

@app.errorhandler(404)
def status_404(error):
    return "<h1>pagina no encontrada</h1>", 404

if __name__ == '__main__':
    app.run(debug=True)
