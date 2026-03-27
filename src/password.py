import secrets
import string

# 定数
# 記号の定数
COMMON_SYMBOLS = "!@#$%^&*()_+-=[]{}"

# 関数
# パスワード生成ロジック
def generate_password(length, use_uppercase, use_lowercase, use_digit, use_symbols):
    alphabet = ""
    if use_uppercase:
        alphabet += string.ascii_uppercase
    if use_lowercase:
        alphabet += string.ascii_lowercase
    if use_digit:
        alphabet += string.digits
    if use_symbols:
        alphabet += COMMON_SYMBOLS
    if not alphabet:
        raise ValueError("文字の種類を1つ以上選択してください")

    return ''.join(secrets.choice(alphabet) for _ in range(length))
