import pytest
import string
from password import generate_password

def test_password_length():
    """指定した長さのパスワードが生成されること"""
    password = generate_password(12, True, True, True, True)
    assert len(password) == 12

def test_uppercase_only():
    """大文字のみ有効のとき、大文字だけで構成されること"""
    password = generate_password(20, True, False, False, False)
    assert all(c in string.ascii_uppercase for c in password)

def test_lowercase_only():
    """小文字のみ有効のとき、小文字だけで構成されること"""
    password = generate_password(20, False, True, False, False)
    assert all(c in string.ascii_lowercase for c in password)

def test_digits_only():
    """数字のみ有効のとき、数字だけで構成されること"""
    password = generate_password(20, False, False, True, False)
    assert all(c in string.digits for c in password)

def test_empty_alphabet_raises_Value_error():
    """全オフのとき、ValueErroeが発生すること"""
    with pytest.raises(ValueError):
        generate_password(12, False, False, False, False)