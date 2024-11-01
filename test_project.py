from project import register_user
from project import user_verification
from project import connect_now
import pytest


# Tests user regsitration
def test_register_user():
    with pytest.raises(ValueError):
        assert register_user("pass", "pass1", "username")


# Test user login in
def test_user_verification():
    with pytest.raises(ValueError):
        assert user_verification("?<NOTAUSER#&^>123", "password")


def test_connect_now():
    with pytest.raises(ValueError):
        assert connect_now("127.0.0.2", "9999", "connect_btn", "username")
