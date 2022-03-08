from fastapi.testclient import TestClient

from libaccount.models.requestresponse.response import RegisterLoginResponse
from libshared.utils import generate_new_token
from tests.integration.account.test_register_login import REGISTER_PAYLOAD, LOGIN_PAYLOAD


new_password = generate_new_token(size_in_bytes=13)
UPDATE_DISPLAY_NAME_PAYLOAD = {
    'display_name': generate_new_token(size_in_bytes=13)
}
UPDATE_PICTURE_PAYLOAD = {
    'picture': 'https://i.imgflip.com/szq6q.jpg'
}
UPDATE_PASSWORD_PAYLOAD = {
    'password': '',
    'password1': new_password,
    'password2': new_password
}


def test_update_display_name(app_account: TestClient):
    """
    GIVEN updating a user's display name
    WHEN the endpoint is called
    THEN it should update the display name and returns a RegisterLoginResponse
    """
    register_payload = REGISTER_PAYLOAD.copy()
    register_payload.update({
        'email': f'{generate_new_token(size_in_bytes=10)}@tradebro.com'
    })
    response = app_account.post('/me/register', json=register_payload)

    resp_body = response.json()
    modeled = RegisterLoginResponse(**resp_body)

    assert response.status_code == 200
    assert modeled

    headers = {
        'authorization': f'Bearer {modeled.access_token}'
    }
    response = app_account.put('/me', json=UPDATE_DISPLAY_NAME_PAYLOAD, headers=headers)

    assert response.status_code == 200

    resp_body = response.json()
    modeled = RegisterLoginResponse(**resp_body)

    assert modeled
    assert modeled.display_name == UPDATE_DISPLAY_NAME_PAYLOAD.get('display_name')


def test_update_picture(app_account: TestClient):
    """
    GIVEN updating a user's picture
    WHEN the endpoint is called
    THEN it should update the picture and returns a RegisterLoginResponse
    """
    register_payload = REGISTER_PAYLOAD.copy()
    register_payload.update({
        'email': f'{generate_new_token(size_in_bytes=10)}@tradebro.com'
    })
    response = app_account.post('/me/register', json=register_payload)

    resp_body = response.json()
    modeled = RegisterLoginResponse(**resp_body)

    assert response.status_code == 200
    assert modeled

    headers = {
        'authorization': f'Bearer {modeled.access_token}'
    }
    response = app_account.put('/me', json=UPDATE_PICTURE_PAYLOAD, headers=headers)

    assert response.status_code == 200

    resp_body = response.json()
    modeled = RegisterLoginResponse(**resp_body)

    assert modeled
    assert modeled.picture == UPDATE_PICTURE_PAYLOAD.get('picture')


def test_update_password(app_account: TestClient):
    """
    GIVEN updating a user's password
    WHEN the endpoint is called
    THEN it should update the password
    """
    register_payload = REGISTER_PAYLOAD.copy()
    register_payload.update({
        'email': f'{generate_new_token(size_in_bytes=10)}@tradebro.com'
    })
    response = app_account.post('/me/register', json=register_payload)

    existing_password = register_payload.get('password1')

    resp_body = response.json()
    modeled = RegisterLoginResponse(**resp_body)

    assert response.status_code == 200
    assert modeled

    headers = {
        'authorization': f'Bearer {modeled.access_token}'
    }
    UPDATE_PASSWORD_PAYLOAD.update({
        'password': existing_password
    })
    response = app_account.put('/me', json=UPDATE_PASSWORD_PAYLOAD, headers=headers)

    assert response.status_code == 200

    resp_body = response.json()
    modeled = RegisterLoginResponse(**resp_body)

    assert modeled

    login_payload = LOGIN_PAYLOAD.copy()
    login_payload.update({
        'email': modeled.email,
        'password': UPDATE_PASSWORD_PAYLOAD.get('password1')
    })
    response = app_account.post('/me/login', json=login_payload)

    assert response.status_code == 200
