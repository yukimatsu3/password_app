import pytest
import services.database as database
from services.database import (
    load_passwords,
    add_password,
    update_password,
    delete_password
)

@pytest.fixture
def init_json(monkeypatch, tmp_path):
    test_file = tmp_path / "passwords.json"
    test_file.write_text("[]", encoding="utf-8")

    monkeypatch.setattr(database, "JSON_PATH", str(test_file))

    return test_file

def test_load_passwords(init_json):
    """パスワードが正しく読み込まれること"""
    data = load_passwords()
    assert isinstance(data, list)
    assert data == []

def test_add_passwords(init_json):
    """パスワードが正しく追加されること"""
    add_password("Google", "test123", "pass1234")
    data = load_passwords()
    assert isinstance(data, list)
    assert data[0]["name"] == "Google"

def test_update_password(init_json):
    """パスワードが正しく更新されること"""
    entry = add_password("Google", "test123", "pass1234")
    update_password(entry["uuid"], "Facebook", "test456", "pass5678")
    data = load_passwords()
    assert isinstance(data, list)
    assert data[0]["name"] == "Facebook"
    assert data[0]["id"] == "test456"
    assert data[0]["pass"] == "pass5678"

def test_delete_password(init_json):
    """パスワードが正しく削除されること"""
    entry = add_password("Google", "test123", "pass1234")
    delete_password(entry["uuid"])
    data = load_passwords()
    assert isinstance(data, list)
    assert data == []

def test_load_passwords_correted_json(monkeypatch, tmp_path):
    """JSONが壊れているとき空リストを返し初期化すること"""
    test_file = tmp_path / "password.json"
    test_file.write_text("invaild json{{", encoding="utf-8")

    monkeypatch.setattr(database, "JSON_PATH", str(test_file))

    data = load_passwords()
    assert data == []

    # バックアップが作られていること
    backup = tmp_path / "password.json.bak"
    assert backup.exists()

    # 初期化後は正常に読み込めること
    data_after = load_passwords()
    assert data_after == []