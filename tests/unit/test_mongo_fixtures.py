from pytest_mongodb import plugin


def test_fixtures_are_loaded(mongodb):
    """
    GIVEN Fixtures are created
    WHEN getting collection names and details
    THEN the collections must include the fixtures we defined
    """
    collection_names = mongodb.list_collection_names()

    assert 'users' in collection_names
    assert 'trades' in collection_names
    assert len(plugin._cache.keys()) == 2

    # Test Users
    assert mongodb.users.count_documents({}) == 2
    user1 = mongodb.users.find_one({'email': 'batista@bango29.com'})
    user2 = mongodb.users.find_one({'email': 'tistaharahap@bango29.com'})
    assert user1 is not None and user2 is not None
    assert user1.get('display_name') == 'Tista'
    assert user2.get('display_name') == 'Tistaharahap'

    # Test Trades
    assert mongodb.trades.count_documents({}) == 2
    trade1 = mongodb.trades.find_one({'user_id': user1.get('_id')})
    trade2 = mongodb.trades.find_one({'user_id': user2.get('_id')})
    assert trade1 is not None and trade2 is not None
    assert trade1.get('exchange') == 'binance-coin-m'
    assert trade2.get('exchange') == 'binance-usdt-m'

