import flet as ft
from services.database import load_passwords, add_password, update_password, delete_password, create_json

def manage_view(page: ft.Page) -> ft.Container:
    create_json()

    return ft.Container()