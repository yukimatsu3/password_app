import os
import json
import shutil
import uuid
import tempfile
import logging
from pathlib import Path

APP_NAME = "PasswordManager"

DATA_DIR = Path(os.environ["APPDATA"]) / APP_NAME
DATA_DIR.mkdir(parents=True, exist_ok=True)

JSON_PATH = DATA_DIR / "passwords.json"

def find_latest_backup():
    """存在する中で一番新しいバックアップパスを返す"""
    backup = JSON_PATH.with_suffix(".json.bak1")
    return backup if backup.exists() else None

# JSONファイル作成
def create_json():
    """
    passwords.jsonが存在しない場合の初期化処理
    - bak1があればそれをコピーして復元
    - なければ空のJSONを作成
    """
    if JSON_PATH.exists():
        return

    logging.info("password.jsonがないため初期化処理を実行")

    bak1 = JSON_PATH.with_suffix(".json.bak1")
    if bak1.exists():
        logging.info(f"bak1から復元します")
        shutil.copyfile(bak1, JSON_PATH)
        return

    # バックアップもない場合は空で作成
    logging.warning("バックアップが見つからないため空のJSONを作成")
    with JSON_PATH.open("w", encoding="utf-8") as f:
        json.dump([], f, indent=4, ensure_ascii=False)

# JSONファイルの読み込み
def load_passwords():
    # 初回起動時
    if not JSON_PATH.exists():
        create_json()

    """passwords.jsonを読み込みpythonオブジェクトとして返す"""
    try:
        with JSON_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)
    # JSONファイルが壊れていたらバックアップファイルを作って空のJSONを作成
    except json.JSONDecodeError:
        logging.warning("JSONが壊れているためbak1から復元を試みます")

        bak1 = JSON_PATH.with_suffix(".json.bak1")
        if bak1.exists():
            shutil.copyfile(bak1, JSON_PATH)
            return load_passwords()

        #  bak1もない場合は空で初期化
        save_passwords([])
        return []
    
    except Exception:
        logging.exception("password.json 読み込み中に想定外のエラーが発生しました")
        return []

# 保存前にバックアップを最大3つ取る
def rotate_backups(max_backups=3):
    for i in range(max_backups - 1, 0, -1):
        src = JSON_PATH.with_suffix(f".json.bak{i}")
        dst = JSON_PATH.with_suffix(f".json.bak{i + 1}")
        if src.exists():
            shutil.copyfile(src, dst)

    # 現在のjsonをbak1としてコピー
    if JSON_PATH.exists():
        shutil.copyfile(
            JSON_PATH,
            JSON_PATH.with_suffix(".json.bak1")
        )

# JSONファイルへの書き込み
# まず一時ファイル（xxx.tmp）に書き込み
# 書き込みが終わってから本番ファイルへ差し替え
# 書き込み途中のファイル破損を防ぐ
def save_passwords(data):
    # 保存前にバックアップ
    rotate_backups()

    """dataをpasswords.jsonに書き込む"""
    try:
        dir_path = JSON_PATH.parent
        with tempfile.NamedTemporaryFile("w", dir=dir_path, delete=False, suffix=".tmp", encoding="utf-8") as tmp:
            json.dump(data, tmp, indent=4, ensure_ascii=False)
            tmp_path = tmp.name

        os.replace(tmp_path, JSON_PATH)
        logging.info("password.jsonを保存しました")
    except Exception:
        logging.exception("password.json 保存中にエラーが発生しました")
        raise

# idの生成
def generate_uuid():
    return str(uuid.uuid4())

# 新しいパスワードを新規追加
def add_password(name, user_id, password):
    data = load_passwords()

    new_entry = {
        "uuid": generate_uuid(),
        "name": name,
        "id": user_id,
        "pass": password,
    }

    data.append(new_entry)
    save_passwords(data)

    return new_entry

# パスワードの更新
def update_password(uuid_value, new_name, new_id, new_password):
    data = load_passwords()

    for item in data:
        if item["uuid"] == uuid_value:
            item["name"] = new_name
            item["id"] = new_id
            item["pass"] = new_password
            break

    save_passwords(data)

# パスワードの削除
def delete_password(uuid_value):
    data = load_passwords()

    data = [item for item in data if item["uuid"] != uuid_value]

    save_passwords(data)