# Games Collection

A collection of 15 arcade and puzzle games built with Python and pygame. Windows and macOS users can grab a pre-built release and play straight away. Linux users and anyone who prefers running from source just need Python and pygame.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![pygame](https://img.shields.io/badge/pygame-2.0%2B-green) ![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

---

## Screenshots

<p align="center">
  <img src="screenshots/menu.png" alt="Menu" width="800"/>
  <br/><em>Main Menu</em>
</p>

| | | |
|:---:|:---:|:---:|
| <img src="screenshots/dodge_game.png" alt="Dodge Game" width="260"/> | <img src="screenshots/snake.png" alt="Snake" width="260"/> | <img src="screenshots/space_asteroids.png" alt="Space Asteroids" width="260"/> |
| <p align="center">Dodge Game</p> | <p align="center">Snake</p> | <p align="center">Space Asteroids</p> |
| <img src="screenshots/space_defenders.png" alt="Space Defenders" width="260"/> | <img src="screenshots/helicopter_dash.png" alt="Helicopter Dash" width="260"/> | <img src="screenshots/hyper_bounce.png" alt="Hyper Bounce" width="260"/> |
| <p align="center">Space Defenders</p> | <p align="center">Helicopter Dash</p> | <p align="center">Hyper Bounce</p> |
| <img src="screenshots/stack_attack.png" alt="Stack Attack" width="260"/> | <img src="screenshots/maze_explorer.png" alt="Maze Explorer" width="260"/> | <img src="screenshots/mine_field.png" alt="Mine Field" width="260"/> |
| <p align="center">Stack Attack</p> | <p align="center">Maze Explorer</p> | <p align="center">Mine Field</p> |
| <img src="screenshots/sudoku.png" alt="Sudoku" width="260"/> | <img src="screenshots/hangman.png" alt="Hangman" width="260"/> | <img src="screenshots/2048.png" alt="2048" width="260"/> |
| <p align="center">Sudoku</p> | <p align="center">Hangman</p> | <p align="center">2048</p> |
| <img src="screenshots/solitaire.png" alt="Solitaire" width="260"/> | <img src="screenshots/spider_solitaire.png" alt="Spider Solitaire" width="260"/> | <img src="screenshots/tripeaks.png" alt="TriPeaks" width="260"/> |
| <p align="center">Solitaire</p> | <p align="center">Spider Solitaire</p> | <p align="center">TriPeaks</p> |

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
git clone https://github.com/veddegre/python-games-collection.git
cd python-games-collection

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

### Linux desktop shortcut

To add Games Collection to your application menu or desktop:

```bash
# Make the launcher executable
chmod +x GameCollection.command

# Copy the .desktop file to your applications menu
cp GameCollection.desktop ~/.local/share/applications/

# Or place a shortcut on your desktop
cp GameCollection.desktop ~/Desktop/
chmod +x ~/Desktop/GameCollection.desktop
```

You may need to edit `GameCollection.desktop` first to set the correct path:
```bash
# Open it and update the Exec and Icon paths to match where you put the folder
nano GameCollection.desktop
```

The relevant lines to update:
```
Exec=python3 /path/to/games-collection/run.py
Icon=/path/to/games-collection/icon.png
Path=/path/to/games-collection
```

### Pre-built releases (Windows and macOS)

Head to the [Releases page](https://github.com/veddegre/python-games-collection/releases) and download the file for your platform.

**Windows**
1. Download `GamesCollection-setup.exe`
2. Run it — you may see a SmartScreen warning. Click **More info** → **Run anyway**
3. Follow the installer wizard (Next → Next → Install → Finish)
4. A shortcut appears on your Desktop and in the Start Menu under **Games Collection**
5. To uninstall: Start Menu → Games Collection → Uninstall, or via Add/Remove Programs

**macOS**
1. Download `GamesCollection-mac.dmg`
2. Double-click to open the disk image
3. Drag **GamesCollection** into the **Applications** folder shortcut
4. Eject the disk image
5. Open from your Applications folder or Launchpad
6. First launch only: right-click the app → **Open** → **Open** (Gatekeeper warning — safe to proceed)
7. After that it opens normally with a double-click

**Linux**
No pre-built app is available for Linux. Follow the Installation steps below — you just need Python and pygame.

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
├── app.manifest             ← Windows UTF-8 manifest (fixes card suit symbols)
├── requirements.txt
├── .gitignore               ← excludes scores.json and __pycache__
├── GameCollection.bat       ← Windows source launcher
├── GameCollection.command   ← macOS source launcher
└── GameCollection.desktop   ← Linux source launcher
```

`scores.json` is created automatically on first play and is excluded from git — each player keeps their own scores.

---

## Notes

- **Windows SmartScreen warning** — Windows may show "Windows protected your PC" the first time you run the installer. Click "More info" → "Run anyway". This happens because the app isn't commercially signed. It's safe to proceed.
- **macOS Gatekeeper warning** — On first launch, right-click the app → Open → Open. After that it launches normally.
- **`scores.json`** stores high scores locally. It is in `.gitignore` so it won't be committed.
- **`__pycache__`** is suppressed via `python -B` in the launcher scripts.
- The bundled Mac `.app` uses the custom icon. If running from source via `python run.py` the Dock will show the Python logo instead — that's expected for unsigned scripts.

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
