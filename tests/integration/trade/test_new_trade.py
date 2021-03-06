from fastapi.testclient import TestClient

from libtrade.models.requestresponse.response import TradeResponse
from libaccount.models.requestresponse.response import RegisterLoginResponse
from libshared.utils import generate_new_token
from tests.integration.account.test_register_login import REGISTER_PAYLOAD


NEW_TRADE_PAYLOAD = {
    'exchange': 'binance-usdt-m',
    'pair': 'BNBUSDT',
    'trade_snapshot': 'https://www.tradingview.com/x/tbVzMBIc/',
    'reason_for_entry': 'Double bottom shown on the chart',
    'reason_for_exit': 'EMA528 as the target is reached',
    'direction': 'long',
    'entry_price': '367.21',
    'exit_price': '388.18',
    'leverage': 10,
    'pnl_in_percent': '57.1',
    'pnl_in_currency': '13029.22',
    'entry_at': '2022-03-07T19:03:03Z',
    'exit_at': '2022-03-08T11:03:03Z',
}


def test_create_new_trade_success(app_client: TestClient):
    """
    GIVEN a user is posting a new trade
    WHEN the endpoint is called
    THEN it should record the trade in the database
    """
    register_payload = REGISTER_PAYLOAD.copy()
    register_payload.update({'email': f'{generate_new_token(size_in_bytes=10)}@tradebro.com'})
    response = app_client.post('/me/register', json=register_payload)

    resp_body = response.json()
    modeled = RegisterLoginResponse(**resp_body)

    assert response.status_code == 200
    assert modeled

    headers = {'authorization': f'Bearer {modeled.access_token}'}
    response = app_client.post('/trades', json=NEW_TRADE_PAYLOAD, headers=headers)

    resp_body = response.json()
    modeled = TradeResponse(**resp_body)

    assert response.status_code == 200
    assert modeled


def test_create_new_trade_without_token(app_client: TestClient):
    """
    GIVEN a user is posting a new trade
    WHEN the endpoint is called without a bearer token
    THEN it should respond with a 401 status code
    """
    response = app_client.post('/trades', json=NEW_TRADE_PAYLOAD)

    assert response.status_code == 401
