# Games Collection

A collection of 15 arcade and puzzle games built with Python and pygame. Launch everything from a single menu — no installation beyond Python and pygame required.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![pygame](https://img.shields.io/badge/pygame-2.0%2B-green) ![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

---

## Screenshots

![Menu](screenshots/menu.png)

| | | |
|---|---|---|
| ![Dodge Game](screenshots/dodge_game.png) | ![Snake](screenshots/snake.png) | ![Space Asteroids](screenshots/space_asteroids.png) |
| ![Space Defenders](screenshots/space_defenders.png) | ![Helicopter Dash](screenshots/helicopter_dash.png) | ![Hyper Bounce](screenshots/hyper_bounce.png) |
| ![Stack Attack](screenshots/stack_attack.png) | ![Maze Explorer](screenshots/maze_explorer.png) | ![Mine Field](screenshots/mine_field.png) |
| ![Sudoku](screenshots/sudoku.png) | ![Hangman](screenshots/hangman.png) | ![2048](screenshots/2048.png) |
| ![Solitaire](screenshots/solitaire.png) | ![Spider Solitaire](screenshots/spider_solitaire.png) | ![TriPeaks](screenshots/tripeaks.png) |

---

## Games

### Action
| Game | Description | Controls |
|------|-------------|----------|
| **Dodge Game** | Dodge falling objects. Speed increases with score. | ← → arrows |
| **Snake** | Eat fruit and grow. Don't hit yourself. | Arrow keys |
| **Space Asteroids** | Shoot rotating asteroids before they hit you. | ← →, Space to shoot |
| **Space Defenders** | Waves of enemies. Watch for the boss at 20pts! | ← →, Space to shoot |
| **Helicopter Dash** | Hold to thrust through a twisting cave. How far can you go? | Hold Space or click |
| **Hyper Bounce** | Smash energy cells with an electric ball across 8 unique levels. | ← →, Space to launch |

### Puzzle
| Game | Description | Controls |
|------|-------------|----------|
| **Stack Attack** | Stack falling blocks and clear rows. Deep space theme with hold piece and combos. | Arrows, Space, C hold, P pause |
| **Maze Explorer** | Navigate a random maze in as few moves as possible. | Arrow keys |
| **Mine Field** | Clear the minefield. First click is always safe. | Left click, right click to flag |
| **Sudoku** | Fill the grid. Every row, column and box needs 1–9. Three difficulty levels. | Click cell, type number |
| **Hangman** | Guess the word before the man is hung. Easy, Medium and Hard word lists. | Type letters or click keyboard |
| **2048** | Merge tiles to reach 2048. Simple to learn, hard to master. | Arrow keys or WASD |

### Cards
| Game | Description | Controls |
|------|-------------|----------|
| **Solitaire** | Classic Klondike. Build foundations from Ace to King. | Click to move, double-click to foundation |
| **Spider Solitaire** | Build 8 K-to-A runs. Choose from 1, 2 or 4 suit difficulty. | Click to select and move |
| **TriPeaks** | Clear three peaks by playing cards ±1 from the waste pile. | Click free cards |

All games save high scores locally to `scores.json` and support **ESC to return to the menu**.

---

## Requirements

- Python 3.8 or newer
- pygame 2.0 or newer

---

## Installation

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/games-collection.git
cd games-collection

# 2. Install pygame
pip install pygame

# 3. Run
python run.py
```

---

## Running

### Command line
```bash
python run.py
```

Any game can also be launched standalone:
```bash
python snake_game.py
python sudoku.py
python hyper_bounce.py
# etc.
```

### Desktop shortcut

| Platform | File | Notes |
|----------|------|-------|
| **Windows** | `GameCollection.bat` | Double-click to launch |
| **macOS** | `GameCollection.command` | First run: right-click → Open (Gatekeeper) |
| **Linux** | `GameCollection.desktop` | May need `chmod +x GameCollection.desktop` |

---

## Project structure

```
games-collection/
├── run.py                   ← entry point
├── menu.py                  ← game launcher and menu
├── highscores.py            ← shared score tracking
├── icon.png                 ← window icon
│
├── Action games
│   ├── dodge_game.py
│   ├── snake_game.py
│   ├── space_asteroids.py
│   ├── space_defenders.py
│   ├── helicopter_dash.py
│   └── hyper_bounce.py
│
├── Puzzle games
│   ├── stack_attack.py
│   ├── maze_explorer.py
│   ├── mine_field.py
│   ├── sudoku.py
│   ├── hangman.py
│   └── game2048.py
│
├── Card games
│   ├── solitaire.py
│   ├── spider_solitaire.py
│   └── tripeaks.py
│
├── words_easy.txt           ← Hangman word lists
├── words_medium.txt
├── words_hard.txt
│
├── screenshots/             ← menu and game screenshots
│
├── requirements.txt
├── .gitignore               ← excludes scores.json and __pycache__
├── GameCollection.bat
├── GameCollection.command
└── GameCollection.desktop
```

`scores.json` is created automatically on first play and is excluded from git — each player keeps their own scores.

---

## Notes

- **`scores.json`** stores high scores locally. It is in `.gitignore` so it won't be committed.
- **`__pycache__`** is suppressed via `python -B` in the launcher scripts.
- The Dock icon on macOS will show the Python logo rather than the custom icon. This is a macOS limitation for unsigned scripts — packaging with PyInstaller into a `.app` bundle would fix it.
- Original games: Dodge Game, Snake, Space Asteroids, Space Defenders, Maze Explorer, Mine Field, Solitaire, Spider Solitaire, TriPeaks, Sudoku, Hangman, 2048.
- New games built for this collection: Stack Attack, Helicopter Dash, Hyper Bounce.

---

## About this project

This started as a personal project to mess around with Python and AI-assisted coding — and ended up as something my kids and I could actually sit down and play together without needing wifi, a subscription, or an app store. Nothing fancy, just a bunch of games that run locally and don't phone home.

If you find it useful, fun, or want to build on it, go for it.

---

## Disclaimer

This is a hobby project made for personal and family use. It's provided as-is — no guarantees, no warranties, no support obligations. Run it at your own risk, though the worst that's likely to happen is a Python error.

---

## License

MIT — do whatever you like with it.
