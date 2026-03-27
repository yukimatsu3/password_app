import flet as ft
from password import generate_password

def main(page: ft.Page):
    # ページの設定
    page.title = "パスワード生成・管理アプリ"
    page.theme_mode = "light"
    page.window.width = 800
    page.window.height = 400

    # 関数
    # 生成ボタンを押したときの処理
    def on_gererate_click(e):
        try:
            password_field.value = generate_password(
                int(slider.value),
                uppercase_checkbox.value,
                lowercase_checkbox.value,
                digit_checkbox.value,
                symbols_checkbox.value
            )
        except ValueError as ex:
            page.show_dialog(ft.SnackBar(ft.Text(str(ex))))
        page.update()

    # コピーボタンを押したときの処理
    async def copy_button_click(e):
        if not password_field.value:
            page.show_dialog(ft.SnackBar("パスワードがまだ生成されていません！"))
        else:
            await ft.Clipboard().set(password_field.value)
            page.show_dialog(ft.SnackBar("パスワードがコピーされました！"))
        page.update()

    # テキストフィールドのクリア
    def on_clear_click(e):
        if not password_field.value:
            page.show_dialog(ft.SnackBar(ft.Text("パスワードがまだ生成されていません！")))
        else:
            password_field.value = ""
        page.update()

    # パスワード文字数スライダー
    def password_number_changed(e):
        lenght_label.value = f"長さ: {slider.value}"
        page.update()

    # UIパーツ
    # パスワード表示フィールド
    password_field = ft.TextField(label="Password", text_size=20, read_only=True, expand=True)

    # 文字制御チェックボックス
    uppercase_checkbox = ft.Checkbox(label="大文字を含む", value=True)
    lowercase_checkbox = ft.Checkbox(label="小文字を含む", value=True)
    digit_checkbox = ft.Checkbox(label="数字を含む", value=True)
    symbols_checkbox = ft.Checkbox(label="記号を含む", value=True)

    # 文字数スライダー
    lenght_label = ft.Text(f"長さ: 12")
    slider = ft.Slider(min=8, max=20, divisions=12, value=12, on_change=password_number_changed)

    # ボタン
    generate_button = ft.Button(content="生成", width=120, on_click=on_gererate_click)
    copy_button = ft.Button(content="コピー", width=120, on_click=copy_button_click)
    clear_button = ft.Button(content="クリア", width=120, on_click=on_clear_click)

    # 初期生成パスワード
    password_field.value = generate_password(
        int(slider.value),
        uppercase_checkbox.value,
        lowercase_checkbox.value,
        digit_checkbox.value,
        symbols_checkbox.value
    )

    page.add(
        ft.Column(
            controls=[
                ft.Row(controls=[
                    lenght_label,
                    slider
                    ],
                alignment=ft.MainAxisAlignment.CENTER
                )
            ],
        ),
        ft.Column(
            controls=[
                ft.Row(controls=[
                    uppercase_checkbox,
                    lowercase_checkbox,
                    digit_checkbox,
                    symbols_checkbox,
                ],
                alignment=ft.MainAxisAlignment.CENTER
                )
            ],
        ),
        ft.Row(
            controls=[
                password_field,
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.Row(
            controls=[
                generate_button,
                copy_button,
                clear_button
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

ft.run(main)