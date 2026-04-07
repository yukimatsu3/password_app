import flet as ft
from services.password import generate_password
from views.generate_view import generate_view
from views.manage_view import manage_view

def main(page: ft.Page):
    # ページの設定
    page.title = "パスワード生成・管理アプリ"
    page.theme_mode = "light"
    page.window.width = 450
    page.window.height = 600
    page.bgcolor = "#ffffff"

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
            generate_view(page),
            manage_view(page),
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

ft.run(main)