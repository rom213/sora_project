import pytest
from app import app
from models import db

@pytest.fixture(scope='module')
def test_client():
    """
    Configura la aplicación en modo de prueba y proporciona un cliente de prueba.
    """
    # Cargar la configuración de Testing
    flask_app = app
    flask_app.config.from_object('config.DevelopmentConfig')  # Usar TestingConfig
    flask_app.config['TESTING'] = True
    flask_app.config['WTF_CSRF_ENABLED'] = False  # Desactivar CSRF para pruebas

    testing_client = flask_app.test_client()

    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()  # Limpiar el contexto al final

@pytest.fixture(scope='module')
def init_database():
    db.create_all()
    yield db  
    db.drop_all()

