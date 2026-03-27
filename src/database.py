import os
import json
import uuid

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
    except json.JSONDecodeError:
        print("JSONファイルが壊れているため初期化します")
        save_passwords([])
        return []

# JSONファイルへの書き込み
def save_passwords(data):
    """dataをpasswords.jsonに書き込む"""
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

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

if __name__ == "__main__":
    create_json()

    # パスワード追加テスト
    entry = add_password("Google", "abc@def.com", "pass1234")
    print("追加:", entry)

    # データの読み込み
    print("読込:", load_passwords())

    # 更新テスト
    update_password(entry["uuid"], "Facebook", "new@def.com", "newpass1234")
    print("更新", load_passwords())

    # 削除テスト
    delete_password(entry["uuid"])
    print("削除:", load_passwords())