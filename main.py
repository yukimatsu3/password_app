import flet as ft
import sys
from pathlib import Path
from main_view import main

def get_base_dir() -> Path:
    # PyInstallerでexe化されている場合
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    # 通常のpython実行時
    return Path.cwd()

def wrapped_main(page: ft.Page):
    base_dir = get_base_dir()
    icon_path = base_dir / "app.ico"

    page.window.icon = str(icon_path)
    main(page)

if __name__ == "__main__":
    ft.run(wrapped_main)
