import pytest
from fastapi.testclient import TestClient

from appbackend.web import app


@pytest.fixture(scope='session')
def app_client():
    return TestClient(app=app)
