import pytest
from fastapi.testclient import TestClient

from appaccount.web import app as account_app


@pytest.fixture(scope='session')
def app_account():
    return TestClient(app=account_app)
