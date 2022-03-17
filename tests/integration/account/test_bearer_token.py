from fastapi.testclient import TestClient

from libshared.utils import generate_new_token
from tests.integration.account.test_update_profile import UPDATE_PICTURE_PAYLOAD


def test_unrecognized_access_token(app_client: TestClient):
    """
    GIVEN requesting with an unrecognized bearer token
    WHEN a protected endpoint is called
    THEN it should respond with a 401 status code
    """
    random_token = generate_new_token(size_in_bytes=43)
    headers = {'authorization': f'Bearer {random_token}'}
    response = app_client.put('/me', headers=headers, json=UPDATE_PICTURE_PAYLOAD)

    assert response.status_code == 401
    assert response.headers.get('content-type') == 'application/json'
    assert response.json().get('detail') == 'Unrecognized access token'


def test_wrongly_formatted_access_token(app_client: TestClient):
    """
    GIVEN requesting with an wrongly formatted bearer token
    WHEN a protected endpoint is called
    THEN it should respond with a 401 status code
    """
    random_token = generate_new_token(size_in_bytes=43)
    headers = {'authorization': f'Bearer {random_token} Bearer {random_token}'}
    response = app_client.put('/me', headers=headers, json=UPDATE_PICTURE_PAYLOAD)

    assert response.status_code == 401
    assert response.headers.get('content-type') == 'application/json'
    assert response.json().get('detail') == 'Unrecognized access token'
