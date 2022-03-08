from fastapi.testclient import TestClient

from libtrade.models.requestresponse.response import TradeResponse
from libaccount.models.requestresponse.response import RegisterLoginResponse
from libshared.utils import generate_new_token
from tests.integration.account.test_register_login import REGISTER_PAYLOAD
from tests.integration.trade.test_new_trade import NEW_TRADE_PAYLOAD


def test_get_my_trades_without_since_id(app_account: TestClient, app_trade: TestClient):
    """
    GIVEN a user is posting a new trade
    WHEN the endpoint is called
    THEN it should record the trade in the database
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
    response = app_trade.post('/trades', json=NEW_TRADE_PAYLOAD, headers=headers)

    resp_body = response.json()
    modeled = TradeResponse(**resp_body)

    assert response.status_code == 200
    assert modeled

    response = app_trade.get('/trades', headers=headers)
    resp_body = response.json()
    trades = [TradeResponse(**x) for x in resp_body]

    assert len(trades) == 1


def test_get_my_trades_with_since_id(app_account: TestClient, app_trade: TestClient):
    """
    GIVEN a user is posting a new trade
    WHEN the endpoint is called
    THEN it should record the trade in the database
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
    response = app_trade.post('/trades', json=NEW_TRADE_PAYLOAD, headers=headers)

    resp_body = response.json()
    modeled = TradeResponse(**resp_body)
    since_id = modeled.id

    assert response.status_code == 200
    assert modeled

    response = app_trade.get(f'/trades?since_id={since_id}', headers=headers)
    resp_body = response.json()
    trades = [TradeResponse(**x) for x in resp_body]

    assert len(trades) == 1
