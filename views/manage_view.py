import flet as ft
import logging
from typing import Callable, Tuple
from state import AppState
from services.database import (
    load_passwords,
    add_password,
    update_password,
    delete_password,
    create_json
)

def manage_view(page: ft.Page, state: AppState) -> Tuple[ft.Container, Callable[[], None]]:
    """戻り値：
        - 管理画面のコンテナ
        - 一覧を再描写するための関数 refresh()
    """
    create_json()

    password_list = ft.ListView(expand=True, spacing=8)
    search_field = ft.TextField(
        hint_text = "検索...",
        prefix_icon=ft.Icons.SEARCH,
        border_radius=10,
        height=45,
        content_padding=ft.Padding.symmetric(vertical=0, horizontal=12),
    )

    def get_filtered():
        # ここではJSONを読まずstate.passwordを使用
        data = state.passwords
        # 検索文字列を小文字化
        q = (search_field.value or "").lower()
        # qが含まれるnameまたはidのデータだけ返す
        if q:
            return [p for p in data if q in p["name"].lower() or q in p["id"].lower()]
        return data

    def refresh():
        # 一覧をstateから再構築
        # 検索結果が変わったときやCRUD処理したときに必要
        password_list.controls.clear()
        # get_filtered()で検索条件にあったデータを取得しListViewへ追加
        for entry in get_filtered():
            password_list.controls.append(build_row(entry))
        page.update()

    def open_from_dialog(entry=None):
        name_field = ft.TextField(label="名前", value=entry["name"] if entry else "")
        id_field = ft.TextField(label="ID", value=entry["id"] if entry else "")
        pass_field = ft.TextField(
            label="パスワード",
            value=entry["pass"] if entry else "",
            password=True,
            can_reveal_password=True,
        )

        def on_save(e):
            # strip():文字列の前後から不要な文字（デフォルトでは空白文字）を削除
            if not name_field.value.strip():
                return
            # パスワードが存在すれば編集モードでアップデート
            if entry:
                update_password(entry["uuid"], name_field.value, id_field.value, pass_field.value)
                logging.info(f"管理画面: パスワードを更新しました uuid={entry["uuid"]}")
            # パスワードが存在しなければ新規追加モードでアップデート
            else:
                new_entry = add_password(name_field.value, id_field.value, pass_field.value)
                state.passwords.append(new_entry)
                logging.info(f"管理画面: パスワードを新規追加しました uuid={new_entry["uuid"]}")
            if entry:
                state.reload_from_json()

            page.pop_dialog()
            refresh()

        page.show_dialog(ft.AlertDialog(
            # 追加モード or 編集モードに応じてテキストを変更
            title=ft.Text("新規追加" if not entry else "編集"),
            content=ft.Column(
                controls=[name_field, id_field, pass_field],
                tight=True,
                spacing=12,
                width=300,
            ),
            actions=[
                ft.TextButton("キャンセル", on_click=lambda e: page.pop_dialog()),
                ft.TextButton("保存", on_click=on_save),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        ))

    def open_delete_dialog(entry):
        def on_confirm(e):
            delete_password(entry["uuid"])
            logging.warning(f"管理画面: パスワードを削除しました uuid={entry["uuid"]}")
            state.reload_from_json()
            page.pop_dialog()
            refresh()

        page.show_dialog(ft.AlertDialog(
            title=ft.Text("削除の確認"),
            content=ft.Text(f'{entry["name"]}を削除しますか？'),
            actions=[
                ft.TextButton("キャンセル", on_click=lambda e: page.pop_dialog()),
                ft.TextButton("削除", on_click=on_confirm, style=ft.ButtonStyle(color=ft.Colors.RED)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        ))

    def build_row(entry):
        async def on_copy(e):
            cb = ft.Clipboard()
            page.services.append(cb)
            await cb.set(entry["pass"])
            page.show_dialog(ft.SnackBar("パスワードをコピーしました"))

        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Text(entry["name"], size=15, weight=ft.FontWeight.W_600),
                            ft.Text(entry["id"], size=12, color=ft.Colors.GREY_600),
                        ],
                        spacing=2,
                        expand=True,
                    ),
                    ft.IconButton(icon=ft.Icons.COPY, icon_size=18, on_click=on_copy, tooltip="コピー"),
                    ft.IconButton(icon=ft.Icons.EDIT, icon_size=18, on_click=lambda e: open_from_dialog(entry), tooltip="編集"),
                    ft.IconButton(icon=ft.Icons.DELETE_OUTLINE, icon_size=18, icon_color=ft.Colors.RED_300, on_click=lambda e: open_delete_dialog(entry), tooltip="削除"),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.Padding.symmetric(horizontal=12, vertical=8),
            border_radius=10,
            bgcolor="#FFFAFA",
            shadow=ft.BoxShadow(blur_radius=4, color="#D3D3D3", offset=ft.Offset(0, 2)),
        )

    search_field.on_change = lambda e: refresh()
    state.passwords = load_passwords()
    refresh()

    container = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("パスワード管理", size=22, weight=ft.FontWeight.BOLD),
                search_field,
                password_list,
                ft.Row(
                    controls=[
                        ft.FloatingActionButton(
                            icon=ft.Icons.ADD,
                            bgcolor="1e95d4",
                            on_click=lambda _: open_from_dialog(),
                        )
                    ],
                    alignment=ft.MainAxisAlignment.END,
                ),
            ],
            expand=True,
            spacing=12,
        ),
        expand=True,
        padding=16,
    )

    return container, refresh