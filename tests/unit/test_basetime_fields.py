from datetime import datetime

from tradebro.libshared.models.mongo import BaseDatetimeMeta


def test_created_at_is_now_ish():
    now = datetime.utcnow()
    instance = BaseDatetimeMeta()

    # Assert we have a default created_at
    assert instance.created_at
    assert isinstance(instance.created_at, datetime)

    delta = instance.created_at - now
    assert delta.seconds < 5


def test_updated_at_default_is_none():
    instance = BaseDatetimeMeta()

    assert instance.updated_at is None
