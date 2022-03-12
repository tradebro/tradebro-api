from fastapi.testclient import TestClient

from libaccount.models.requestresponse.response import RegisterLoginResponse
from libshared.utils import generate_new_token

register_email = f'{generate_new_token(size_in_bytes=10)}@tradebro.com'
register_password = generate_new_token(size_in_bytes=30)
REGISTER_PAYLOAD = {
    'email': register_email,
    'password1': register_password,
    'password2': register_password,
    'display_name': 'tista',
    'picture': 'https://pbs.twimg.com/profile_images/1373650624894537730/zTOfiphF_400x400.jpg',
}
REGISTER_EXISTING_EMAIL_PAYLOAD = {
    'email': 'batista@bango29.com',
    'password1': register_password,
    'password2': register_password,
    'display_name': 'tista',
    'picture': 'https://pbs.twimg.com/profile_images/1373650624894537730/zTOfiphF_400x400.jpg',
}
LOGIN_PAYLOAD = {
    'email': register_email,
    'password': register_password,
}


def test_register_success(app_client: TestClient):
    """
    GIVEN registering a new user
    WHEN the endpoint is called
    THEN it should register the user and returns a RegisterLoginResponse
    """
    response = app_client.post('/me/register', json=REGISTER_PAYLOAD)

    resp_body = response.json()
    modeled = RegisterLoginResponse(**resp_body)

    assert response.status_code == 200
    assert modeled


def test_register_existing_email(app_client: TestClient):
    """
    GIVEN registering with an existing email
    WHEN the endpoint is called
    THEN it should reject the request with a 403 status code
    """
    response = app_client.post('/me/register', json=REGISTER_PAYLOAD)

    assert response.status_code == 403


def test_login_success(app_client: TestClient):
    """
    GIVEN logging in a user
    WHEN the endpoint is called
    THEN it should login the user and returns a RegisterLoginResponse
    """
    response = app_client.post('/me/login', json=LOGIN_PAYLOAD)

    resp_body = response.json()
    modeled = RegisterLoginResponse(**resp_body)

    assert response.status_code == 200
    assert modeled


def test_login_incorrect_password(app_client: TestClient):
    """
    GIVEN logging in a user with a wrong password
    WHEN the endpoint is called
    THEN it should reject the request with a 401 status code
    """
    wrong_password_payload = LOGIN_PAYLOAD.copy()
    wrong_password_payload['password'] = 'wrongpassword'
    response = app_client.post('/me/login', json=wrong_password_payload)

    assert response.status_code == 401


def test_login_nonexisting_user(app_client: TestClient):
    """
    GIVEN logging in a user with an unrecognized email
    WHEN the endpoint is called
    THEN it should reject the request with a 401 status code
    """
    wrong_password_payload = LOGIN_PAYLOAD.copy()
    wrong_password_payload['email'] = f'{generate_new_token(size_in_bytes=12)}@bango29.com'
    response = app_client.post('/me/login', json=wrong_password_payload)

    assert response.status_code == 401
