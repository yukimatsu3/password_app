import flet as ft
from state import AppState
from views.generate_view import generate_view
from views.manage_view import manage_view

def main(page: ft.Page):
    # ページの設定
    page.title = "パスワード生成・管理アプリ"
    page.theme_mode = "light"
    page.window.width = 450
    page.window.height = 600
    page.bgcolor = "#ffffff"

    # アプリ全体の状態を用意（起動時にJSONから読み込み）
    app_state = AppState.load_initial()

    # タブバー
    tab_bar = ft.TabBar(
        tabs=[
            ft.Tab(label="パスワード生成"),
            ft.Tab(label="管理画面"),
        ],
        tab_alignment=ft.TabAlignment.CENTER,
    )

    # 管理画面ビューは自分を更新するための関数を外に出せるようにする
    manage_container, manage_refresh = manage_view(page, app_state)

    # タブの中身
    tab_view = ft.TabBarView(
        expand=True,
        controls=[
            # 生成画面にはstateと管理画面を更新するコールバックを渡す
            generate_view(page, app_state, on_saved=manage_refresh),
            manage_container,
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
                tab_view,
            ]
        )
    )

    page.add(tabs)