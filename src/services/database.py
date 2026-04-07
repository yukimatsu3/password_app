import os
import json
import uuid
import tempfile

# このファイルのディレクトリパスを取得
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# このディレクトリの親ディレクトリを取得
BASE_DIR = os.path.dirname(CURRENT_DIR)
# passwords.jsonのパスを作成
JSON_PATH = os.path.join(BASE_DIR, "passwords.json")

# JSONファイル作成
def create_json():
    """passwords.jsonがなければ作成"""
    if not os.path.exists(JSON_PATH):
        print("passwords.jsonがないので新規作成")
        with open(JSON_PATH, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4, ensure_ascii=False)
    else:
        print("passwords.jsonは既に存在しています")

# JSONファイルの読み込み
def load_passwords():
    """passwords.jsonを読み込みpythonオブジェクトとして返す"""
    try:
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    # JSONファイルが壊れていたらバックアップファイルを作って空のJSONを作成
    except json.JSONDecodeError:
        backup_path = JSON_PATH + ".bak"
        os.replace(JSON_PATH, backup_path)
        print(f"JSONファイルが壊れているため {backup_path} にバックアップし初期化します")
        save_passwords([])
        return []

# JSONファイルへの書き込み
# まず一時ファイル（xxx.tmp）に書き込み
# 書き込みが終わってから本番ファイルへ差し替え
# 書き込み途中のファイル破損を防ぐ
def save_passwords(data):
    """dataをpasswords.jsonに書き込む"""
    dir_path = os.path.dirname(JSON_PATH)
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