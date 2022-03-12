from fastapi.testclient import TestClient


def test_hc(app_client: TestClient):
    """
    GIVEN healthcheck endpoint is defined
    WHEN the endpoint is called
    THEN it should return a status code 200 with an "OK" string response
    """
    response = app_client.get('/public/hc')
    assert response.status_code == 200
    assert response.text == '"OK"'
