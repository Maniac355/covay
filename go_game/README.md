# Go – Cờ Vây

A complete Go (Weiqi / Baduk) game built in Python with PySide6.

## Features

- **Board sizes**: 9×9, 13×13, 19×19
- **Full rule compliance**: captures, ko (simple + positional superko), suicide toggle
- **Scoring**: Japanese (Territory) and Chinese (Area) rules with dead-stone marking
- **Beautiful UI**: QPainter-rendered board with shadows, anti-aliasing, ghost stones, last-move marker
- **Undo/Redo**: Multi-step with full state snapshots
- **Save/Load**: JSON format preserving full game history
- **Move History**: Coordinate-based list with standard notation

## Requirements

- Python ≥ 3.10
- PySide6 ≥ 6.5

## Installation

```bash
pip install -r requirements.txt
```

## Running

From the project root directory (parent of `go_game/`):

```bash
python -m go_game.main
```

## Running Tests

```bash
python -m pytest go_game/tests/ -v
```

Or with unittest:

```bash
python -m unittest go_game.tests.test_engine -v
```

## Building an Executable (Windows)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name GoGame go_game/main.py
```

The executable will be in `dist/GoGame.exe`.

## Architecture

```
go_game/
├── engine/           # Pure game logic (no UI dependency)
│   ├── board.py      # Board grid, groups, liberties, territory
│   ├── rules.py      # Move validation, captures, ko detection
│   ├── state.py      # GameState: ties board + rules + history
│   ├── scoring.py    # Japanese and Chinese scoring
│   └── history.py    # Undo/redo with full snapshots
├── ui/               # PySide6 interface
│   ├── theme.py      # Colours, fonts, stylesheets
│   ├── board_widget.py # QPainter board renderer
│   ├── dialogs.py    # New Game, Settings, Score dialogs
│   └── main_window.py # Main window coordination
├── tests/
│   └── test_engine.py # Unit tests for engine
├── main.py           # Entry point
├── requirements.txt
└── README.md
```

### Key Concepts

**Capture**: A group of connected stones is captured (removed from the board) when it has zero liberties (empty adjacent intersections). Captures happen immediately after a stone is placed.

**Ko**: Prevents infinite loops. Simple Ko forbids immediately recapturing a single stone that was just captured. Positional Superko forbids any move that recreates a previous board position.

**Scoring**:
- *Japanese (Territory)*: Score = empty territory surrounded + captures + komi
- *Chinese (Area)*: Score = stones on board + territory surrounded + komi

After both players pass, the game enters Scoring Mode where players mark dead stones. The score is then computed according to the chosen ruleset.
