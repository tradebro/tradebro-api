import pytest
from fastapi.testclient import TestClient

from appaccount.web import app as account_app
from apptrade.web import app as trade_app


@pytest.fixture(scope='session')
def app_account():
    return TestClient(app=account_app)


@pytest.fixture(scope='session')
def app_trade():
    return TestClient(app=trade_app)
