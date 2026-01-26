"""
Entry point for the Go (Cờ Vây) game.

Usage:
    python -m go_game.main
    # or
    python go_game/main.py
"""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from go_game.ui.main_window import MainWindow
from go_game.ui.theme import APP_STYLESHEET


def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationName("Go – Cờ Vây")
    app.setStyleSheet(APP_STYLESHEET)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
