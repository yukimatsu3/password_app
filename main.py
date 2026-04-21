import flet as ft
import logging
import sys
from pathlib import Path
from main_view import main

def get_log_path() -> Path:
    # exeの場合
    if getattr(sys,"frozen", False):
        return Path(sys.executable).parent / "app.log"
    # 通常のpython実行時
    return Path("app.log")

logging.basicConfig(
    filename=get_log_path(),
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8",
    force=True,
)

def get_base_dir() -> Path:
    # PyInstallerでexe化されている場合
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    # 通常のpython実行時
    return Path.cwd()

def wrapped_main(page: ft.Page):
    try:
        logging.info("アプリケーション起動")

        base_dir = get_base_dir()
        icon_path = base_dir / "app.ico"

        page.window.icon = str(icon_path)
        main(page)
    except Exception:
        logging.exception("想定外のエラーが発生しました")

if __name__ == "__main__":
    ft.run(wrapped_main)
