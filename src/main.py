import flet as ft
import secrets
import string

def main(page: ft.Page):
    password_field = ft.TextField(label="Password", text_size=20, read_only=True, expand=True)
    
    # パスワード生成ロジック
    def generate_password():
        alphabet = string.ascii_letters + string.digits + string.punctuation
        return ''.join(secrets.choice(alphabet) for _ in range(12))

    # 生成ボタンを押したときの処理
    def on_gererate_click(e):
        password_field.value = generate_password()
        page.update()
    
    # コピーボタンを押したときの処理
    async def copy_button_click(e):
        if not password_field.value:
            page.show_dialog(ft.SnackBar("パスワードがまだ生成されていません！"))
        else:
            await ft.Clipboard().set(password_field.value)
            page.show_dialog(ft.SnackBar("パスワードがコピーされました！"))

    page.add(
        ft.Row(
            controls=[
                password_field,
                ft.Button(content="生成", width=120, on_click=on_gererate_click),
                ft.Button(content="コピー", width=120, on_click=copy_button_click),
            ]
        )
    )

ft.run(main)