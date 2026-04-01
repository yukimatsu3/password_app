import pytest
import string
from services.password import generate_password

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

def test_symbols_only():
    """記号のみ有効のとき、記号だけで構成されること"""
    from services.password import COMMON_SYMBOLS
    password = generate_password(20, False, False, False, True)
    assert all(c in COMMON_SYMBOLS for c in password)

def test_contains_required_chars():
    """全オンの時、各種類の文字が最低一文字含まれること"""
    from services.password import COMMON_SYMBOLS
    password = generate_password(12, True, True, True, True)
    assert any(c in string.ascii_uppercase for c in password)
    assert any(c in string.ascii_lowercase for c in password)
    assert any(c in string.digits for c in password)
    assert any(c in COMMON_SYMBOLS for c in password)
