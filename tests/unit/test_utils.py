import pytest

from libshared.utils import generate_new_token
from libshared.fastapi import get_basic_app_params


def test_generate_new_token_with_default_param_string_len_is_134():
    """
    GIVEN generate_new_token with no parameters
    WHEN the method is called
    THEN a new random string is generated with exactly 43 characters
    """
    token = generate_new_token()
    assert len(token) == 134


def test_generate_new_token_with_param():
    """
    GIVEN generate_new_token with 50 as the size_in_bytes parameter value
    WHEN the method is called
    THEN a new random string is generated with exactly 43 characters
    """
    token = generate_new_token(size_in_bytes=50)
    assert len(token) == 67


@pytest.mark.raises(exception=TypeError)
def test_generate_new_token_must_be_called_with_kwarg():
    """
    GIVEN generate_new_token called with positional argument
    WHEN the method is called
    THEN a TypeError exception is raised
    """
    generate_new_token(50)
