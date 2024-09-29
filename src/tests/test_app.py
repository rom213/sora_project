from unittest.mock import patch
from flask_login import login_user
from models.entities.User import User


def test_index_requires_login(test_client):
    response = test_client.get('/index')
    assert response.status_code == 302
    assert '/login' in response.location

def test_route_root_requires_login(test_client):
    response = test_client.get('/')
    assert response.status_code == 302
    assert '/login' in response.location

def test_all_requires_login(test_client):
    response = test_client.post('/conexion/all')
    assert response.status_code == 302  # Verificamos que haya un redireccionamiento
    assert '/login' in response.location  # El redireccionamiento debe ser hacia la página de login


def test_all_post_authenticated_user(test_client, init_database):
    mock_user = User(
        anonymous_user='hola',
        email='roma@gmail.com',
        lastname='ariza',
        name='romario',
        password='1234',
        username='roma',
        avatar=''
    )
    
    print(mock_user.is_authenticated)


    with test_client:
        with test_client.session_transaction() as sess:
            sess['_user_id'] = mock_user.id 
        
        with test_client.application.test_request_context():
            login_user(mock_user)

        response = test_client.post('/conexion/all')
        assert response.status_code == 200 