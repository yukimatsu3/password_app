import os
import json
import uuid
import tempfile
from pathlib import Path

APP_NAME = "PasswordManager"

DATA_DIR = Path(os.environ["APPDATA"]) / APP_NAME
DATA_DIR.mkdir(parents=True, exist_ok=True)

JSON_PATH = DATA_DIR / "passwords.json"

""" # このファイルのディレクトリパスを取得
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# このディレクトリの親ディレクトリを取得
BASE_DIR = os.path.dirname(CURRENT_DIR)
# passwords.jsonのパスを作成
JSON_PATH = os.path.join(BASE_DIR, "passwords.json")
 """

# JSONファイル作成
def create_json():
    """passwords.jsonがなければ作成"""
    if not JSON_PATH.exists():
        print("passwords.jsonがないので新規作成")
        with JSON_PATH.open("w", encoding="utf-8") as f:
            json.dump([], f, indent=4, ensure_ascii=False)
    else:
        print("passwords.jsonは既に存在しています")

# JSONファイルの読み込み
def load_passwords():
    # 初回起動時
    if not JSON_PATH.exists():
        create_json()
        return []

    """passwords.jsonを読み込みpythonオブジェクトとして返す"""
    try:
        with JSON_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)
    # JSONファイルが壊れていたらバックアップファイルを作って空のJSONを作成
    except json.JSONDecodeError:
        backup_path = JSON_PATH.with_suffix(".json.bak1")
        if backup_path.exists():
            os.replace(backup_path, JSON_PATH)
            print(f"JSONファイルが壊れているため {backup_path} にバックアップし初期化します")
            return load_passwords()

        #  バックアップがない場合は
        save_passwords([])
        return []

# 保存前にバックアップを最大3つ取る
def rorate_backups(max_backups=2):
    for i in range(max_backups, 0, -1):
        src = JSON_PATH.with_suffix(f".json.bak{i}")
        dst = JSON_PATH.with_suffix(f".json.bak{i + 1}")
        if src.exists():
            os.replace(src, dst)

    if JSON_PATH.exists():
        first_backup = JSON_PATH.with_suffix(".json.bak1")
        os.replace(JSON_PATH, first_backup)

# JSONファイルへの書き込み
# まず一時ファイル（xxx.tmp）に書き込み
# 書き込みが終わってから本番ファイルへ差し替え
# 書き込み途中のファイル破損を防ぐ
def save_passwords(data):
    # 保存前にバックアップ
    rorate_backups()

    """dataをpasswords.jsonに書き込む"""
    dir_path = JSON_PATH.parent
    with tempfile.NamedTemporaryFile("w", dir=dir_path, delete=False, suffix=".tmp", encoding="utf-8") as tmp:
        json.dump(data, tmp, indent=4, ensure_ascii=False)
        tmp_path = tmp.name
    os.replace(tmp_path, JSON_PATH)

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