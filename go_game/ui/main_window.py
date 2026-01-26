"""
Main application window – manages screen transitions.

Uses a QStackedWidget to switch between:
  0 - Main Menu
  1 - Game Setup
  2 - Tutorial (How to Play)
  3 - Game Screen (gameplay)
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFileDialog,
    QMainWindow,
    QStackedWidget,
    QStatusBar,
    QWidget,
)

from ..engine.state import GameConfig, GameState
from .dialogs import show_invalid_move
from .game_screen import GameScreen
from .game_setup import GameSetupScreen
from .main_menu import MainMenuScreen
from .tutorial import TutorialScreen
from . import theme


class MainWindow(QMainWindow):
    """Top-level window – orchestrates screen navigation."""

    # Screen indices
    _MENU = 0
    _SETUP = 1
    _TUTORIAL = 2
    _GAME = 3

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Go – Cờ Vây")
        self.setMinimumSize(950, 680)
        self.resize(1120, 780)

        self._build_screens()
        self._connect_signals()
        self._show_screen(self._MENU)

        # Status bar
        self.setStatusBar(QStatusBar())
        self.statusBar().showMessage("Welcome to Go – Cờ Vây")

    # -----------------------------------------------------------------------
    # Build
    # -----------------------------------------------------------------------

    def _build_screens(self) -> None:
        self._stack = QStackedWidget()
        self._stack.setObjectName("central")
        self.setCentralWidget(self._stack)

        self._menu_screen = MainMenuScreen()
        self._setup_screen = GameSetupScreen()
        self._tutorial_screen = TutorialScreen()
        self._game_screen = GameScreen()

        self._stack.addWidget(self._menu_screen)    # 0
        self._stack.addWidget(self._setup_screen)   # 1
        self._stack.addWidget(self._tutorial_screen) # 2
        self._stack.addWidget(self._game_screen)     # 3

    def _connect_signals(self) -> None:
        # Main menu
        self._menu_screen.new_game_clicked.connect(self._go_to_setup)
        self._menu_screen.load_game_clicked.connect(self._on_load_game)
        self._menu_screen.tutorial_clicked.connect(self._go_to_tutorial)
        self._menu_screen.quit_clicked.connect(self.close)

        # Setup
        self._setup_screen.start_game.connect(self._on_start_game)
        self._setup_screen.back_clicked.connect(self._go_to_menu)

        # Tutorial
        self._tutorial_screen.back_clicked.connect(self._go_to_menu)

        # Game screen
        self._game_screen.back_to_menu.connect(self._go_to_menu)
        self._game_screen.new_game_requested.connect(self._go_to_setup)

    # -----------------------------------------------------------------------
    # Navigation
    # -----------------------------------------------------------------------

    def _show_screen(self, index: int) -> None:
        self._stack.setCurrentIndex(index)

    def _go_to_menu(self) -> None:
        self._show_screen(self._MENU)
        self.statusBar().showMessage("Main Menu")

    def _go_to_setup(self) -> None:
        self._show_screen(self._SETUP)
        self.statusBar().showMessage("Configure your game")

    def _go_to_tutorial(self) -> None:
        self._show_screen(self._TUTORIAL)
        self.statusBar().showMessage("How to Play Go")

    def _go_to_game(self) -> None:
        self._show_screen(self._GAME)
        self.statusBar().showMessage("Game in progress")

    # -----------------------------------------------------------------------
    # Actions
    # -----------------------------------------------------------------------

    def _on_start_game(self, config: GameConfig) -> None:
        self._game_screen.start_game(config)
        self._go_to_game()

    def _on_load_game(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Load Game", "", "Go Game (*.json);;All Files (*)"
        )
        if not path:
            return
        try:
            game = GameState.load_json(path)
            self._game_screen.load_game(game)
            self._go_to_game()
            self.statusBar().showMessage(f"Game loaded from {path}")
        except Exception as e:
            show_invalid_move(self, f"Load failed: {e}")
