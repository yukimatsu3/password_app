import flet as ft
import logging
from state import AppState
from services.password import generate_password
from services.database import add_password, create_json

def generate_view(
        page: ft.Page,
        state: AppState,
        on_saved=None,
        ) -> ft.Container:
    create_json()

    # 生成ボタンを押したときの処理
    def on_generate_click(e):
        logging.info("生成ボタンが押されました")

        try:
            password_field.value = generate_password(
                int(slider.value),
                uppercase_checkbox.value,
                lowercase_checkbox.value,
                digit_checkbox.value,
                symbols_checkbox.value
            )
            logging.info("パスワード生成に成功しました")

        except ValueError as ex:
            logging.warning(f"パスワード生成失敗: {ex}")
            page.show_dialog(ft.SnackBar(ft.Text(str(ex))))

        except Exception:
            logging.exception("パスワード生成処理で想定外のエラーが発生しました")
            page.show_dialog(ft.SnackBar(ft.Text("内部エラーが発生しました")))

        page.update()

    # コピーボタンを押したときの処理
    async def copy_button_click(e):
        if not password_field.value:
            logging.warning("コピーが実行されましたがパスワードが空でした")
            page.show_dialog(ft.SnackBar("パスワードがまだ生成されていません！"))
        else:
            try:
                cb = ft.Clipboard()
                page.services.append(cb)
                await cb.set(password_field.value)
                logging.info("パスワードをクリップボードにコピーしました")
                page.show_dialog(ft.SnackBar("パスワードがコピーされました！"))
            except:
                logging.info("クリップボードへのコピーに失敗しました")
                page.show_dialog(ft.SnackBar("クリップボードへのコピーに失敗しました"))

        page.update()

    # 保存ボタンを押したときの処理
    def on_save_click(e):
        logging.info("保存ボタンが押されました")

        if not password_field.value:
            logging.warning("パスワード保存中にエラーが発生しました")
            page.show_dialog(ft.SnackBar("パスワードがまだ生成されていません！"))
            return

        name_field = ft.TextField(label="名前")
        id_field = ft.TextField(label="ID")

        def on_confirm(e):
            if not name_field.value.strip():
                return
            # JSONに保存
            new_entry =add_password(name_field.value, id_field.value, password_field.value)
            # stateにも反映
            state.passwords.append(new_entry)

            page.pop_dialog()
            page.show_dialog(ft.SnackBar("保存しました"))

            if on_saved is not None:
                on_saved()

        page.show_dialog(ft.AlertDialog(
            title=ft.Text("パスワードを保存"),
            content=ft.Column(
                controls=[name_field, id_field],
                tight=True,
                spacing=12,
                width=300,
            ),
            actions=[
                ft.TextButton("キャンセル", on_click=lambda _: page.pop_dialog()),
                ft.TextButton("保存", on_click=on_confirm),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        ))

    # テキストフィールドのクリア
    def on_clear_click(e):
        if not password_field.value:
            page.show_dialog(ft.SnackBar(ft.Text("パスワードがまだ生成されていません！")))
        else:
            password_field.value = ""
        page.update()

    # パスワード文字数スライダー
    def password_number_changed(e):
        length_label.value = f"長さ: {int(slider.value)}"
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
    length_label = ft.Text(f"長さ: 12", size=16)
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
    save_button = ft.Button(content="保存", width=120, on_click=on_save_click)

    # 初期生成パスワード
    try:
        password_field.value = generate_password(
            int(slider.value),
            uppercase_checkbox.value,
            lowercase_checkbox.value,
            digit_checkbox.value,
            symbols_checkbox.value
        )
    except ValueError:
        password_field.value = ""

    return ft.Container(
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
                ft.Row([length_label , slider], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(
                    content=
                    ft.Row([generate_button], alignment=ft.MainAxisAlignment.CENTER, margin=ft.Margin.only(bottom=60))),
                ft.Container(
                    content=
                    ft.Row([password_field], alignment=ft.MainAxisAlignment.CENTER)),
                ft.Container(
                    content=
                    ft.Row([copy_button, save_button, clear_button], alignment=ft.MainAxisAlignment.CENTER, margin=ft.Margin.only(top=10))
                ),
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        expand=True
    )