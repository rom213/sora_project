from flask import Flask, redirect, url_for
from config import config
from flask_login import LoginManager
from flask_mysqldb import MySQL
from flask_cors import CORS
from models import db
from models.ModelUser import User
from routes import init_app as init_routes

app = Flask(__name__)
CORS(app)

app.config.from_object(config['development'])

# Inicializar SQLAlchemy
db.init_app(app)
with app.app_context():
    db.create_all()

login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

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
    return "<h1>Pagina no encontrada</h1>", 404

if __name__ == '__main__':
    app.run(debug=True,port=5001, host='0.0.0.0')
