import secrets
import string

# 定数
# 記号の定数
COMMON_SYMBOLS = "@#$%^*()_+=&-"

# 関数
# パスワード生成ロジック
def generate_password(length, use_uppercase, use_lowercase, use_digit, use_symbols):
    alphabet = ""

    #大文字・小文字・数字・記号を必ず1文字以上含めるようにする
    #secrets.choiceでランダムに選ばれた1文字だけをrequiredへ追加
    required = []

    if use_uppercase:
        alphabet += string.ascii_uppercase
        required.append(secrets.choice(string.ascii_uppercase))
    if use_lowercase:
        alphabet += string.ascii_lowercase
        required.append(secrets.choice(string.ascii_lowercase))
    if use_digit:
        alphabet += string.digits
        required.append(secrets.choice(string.digits))
    if use_symbols:
        alphabet += COMMON_SYMBOLS
        required.append(secrets.choice(COMMON_SYMBOLS))

    if not alphabet:
        raise ValueError("文字の種類を1つ以上選択してください")

    # チェックが入った文字種からrequired文字数分の数をfor文で繰り返し
    password_chars = required + [secrets.choice(alphabet) for _ in range(length - len(required))]

    # Fisher–Yatesのアルゴリズムを使用して偏りのないランダムな文字列を作成
    # secrets.randbelow() は暗号学的に安全な乱数を生成する関数
    for i in range(len(password_chars) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        password_chars[i], password_chars[j] = password_chars[j], password_chars[i]

    return ''.join(password_chars)
