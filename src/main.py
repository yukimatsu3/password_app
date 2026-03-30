import flet as ft
from password import generate_password

def main(page: ft.Page):
    # ページの設定
    page.title = "パスワード生成・管理アプリ"
    page.theme_mode = "light"
    page.window.width = 450
    page.window.height = 600
    page.bgcolor = "#ffffff"

    # 関数
    # 生成ボタンを押したときの処理
    def on_generate_click(e):
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
    password_field = ft.TextField(label="Password", text_size=20, width=300, read_only=True)

    # 文字制御チェックボックス
    uppercase_checkbox = ft.Checkbox(label="大文字", label_style=ft.TextStyle(size=16), value=True, active_color="#1e95d4")
    lowercase_checkbox = ft.Checkbox(label="小文字", label_style=ft.TextStyle(size=16), value=True, active_color="#1e95d4")
    digit_checkbox = ft.Checkbox(label="数字", value=True, label_style=ft.TextStyle(size=16), active_color="#1e95d4")
    symbols_checkbox = ft.Checkbox(label="記号", value=True, label_style=ft.TextStyle(size=16), active_color="#1e95d4")

    # 文字数スライダー
    lenght_label = ft.Text(f"長さ: 12", size=16)
    slider = ft.Slider(min=8, max=20, divisions=12, value=12, active_color="#1e95d4", on_change=password_number_changed)

    # ボタン
    generate_button = ft.Button(
        content=ft.Text("生成", color="white"),
        width=150,
        bgcolor="#1e95d4",
        on_click=on_generate_click
    )
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

    # パスワード生成タブ
    generate_view = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(
                            content=uppercase_checkbox,
                            alignment=ft.Alignment.CENTER_LEFT,
                            width=150,
                            height=50,
                            border_radius=5,
                            bgcolor="#FFFAFA",
                            shadow=ft.BoxShadow(blur_radius=5, color="#D3D3D3", offset=ft.Offset(0, 2))
                        ),
                        ft.Container(
                            content=lowercase_checkbox,
                            alignment=ft.Alignment.CENTER_LEFT,
                            width=150,
                            height=50,
                            border_radius=5,
                            bgcolor="#FFFAFA",
                            shadow=ft.BoxShadow(blur_radius=5, color="#D3D3D3", offset=ft.Offset(0, 2))
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Row(
                    controls=[
                        ft.Container(
                            content=digit_checkbox,
                            alignment=ft.Alignment.CENTER_LEFT,
                            width=150,
                            height=50,
                            border_radius=5,
                            bgcolor="#FFFAFA",
                            shadow=ft.BoxShadow(blur_radius=5, color="#D3D3D3", offset=ft.Offset(0, 2))
                        ),
                        ft.Container(
                            content=symbols_checkbox,
                            alignment=ft.Alignment.CENTER_LEFT,
                            width=150,
                            height=50,
                            border_radius=5,
                            bgcolor="#FFFAFA",
                            shadow=ft.BoxShadow(blur_radius=5, color="#D3D3D3", offset=ft.Offset(0, 2))
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Row([lenght_label, slider], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(
                    content=
                    ft.Row([generate_button], alignment=ft.MainAxisAlignment.CENTER, margin=ft.Margin.only(bottom=60))),
                ft.Container(
                    content=
                    ft.Row([password_field], alignment=ft.MainAxisAlignment.CENTER)),
                ft.Container(
                    content=
                    ft.Row([copy_button, clear_button], alignment=ft.MainAxisAlignment.CENTER, margin=ft.Margin.only(top=10))
                ),
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        expand=True
    )

    # パスワード管理タブこれから作成
    manage_view = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("パスワード管理画面", size=20)
            ]
        ),
        expand=True
    )

    # タブバー
    tab_bar = ft.TabBar(
        tabs=[
            ft.Tab(label="パスワード生成"),
            ft.Tab(label="管理画面"),
        ],
        tab_alignment=ft.TabAlignment.CENTER,
    )

    # タブの中身
    tab_view = ft.TabBarView(
        expand=True,
        controls=[
            generate_view,
            manage_view,
        ]
    )

    # タブ全体
    tabs = ft.Tabs(
        selected_index=0,
        length=2,
        expand=True,
        content=ft.Column(
            expand=True,
            controls=[
                tab_bar,
                tab_view
            ]
        )
    )


    page.add(tabs)

ft.run(main)