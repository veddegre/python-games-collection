import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import sys
if sys.platform == "win32":
    os.environ["PYTHONUTF8"] = "1"
    try:
        import ctypes
        ctypes.windll.kernel32.SetConsoleOutputCP(65001)
        ctypes.windll.kernel32.SetConsoleCP(65001)
    except Exception:
        pass

from game_runtime import (
    get_script_dir,
    handle_subprocess_game_argv,
    launch_game_subprocess,
    set_window_icon,
    setup_logging,
)

# Child-process --game mode is for source installs only; packaged apps use in-process exec.
if not getattr(sys, "frozen", False):
    handle_subprocess_game_argv()

LOGGER = setup_logging()

import pygame
import time
from highscores import get_all_scores

pygame.init()

WIDTH, HEIGHT = 980, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Games Collection")

set_window_icon()

# Colors
BG_DARK    = (15, 15, 30)
BG_PANEL   = (22, 26, 48)
ACCENT     = (80, 130, 255)
WHITE      = (255, 255, 255)
GRAY       = (120, 120, 140)
GALLOWS    = (200, 190, 170)
ROPE       = (180, 160, 120)
LIGHT_GRAY = (180, 180, 200)
GOLD       = (255, 210, 50)
RED        = (220, 60, 60)
GREEN      = (60, 200, 100)

def _init_fonts():
    global title_font, menu_font, info_font, small_font, score_font
    title_font  = pygame.font.SysFont("Arial", 38, bold=True)
    menu_font   = pygame.font.SysFont("Arial", 17, bold=True)
    info_font   = pygame.font.SysFont("Arial", 15)
    small_font  = pygame.font.SysFont("Arial", 13)
    score_font  = pygame.font.SysFont("Arial", 13, bold=True)

title_font = menu_font = info_font = small_font = score_font = None
_init_fonts()

GAMES = [
    {"name": "Dodge Game",       "file": "dodge_game.py",      "score_key": "dodge_game",
     "score_label": "Best",      "icon_color": (220, 80,  80),  "icon": "dodge",
     "description": "Dodge falling objects. Speed increases with score.",
     "controls": "Left/Right arrows  |  R to restart  |  ESC to menu"},
    {"name": "Snake",            "file": "snake_game.py",       "score_key": "snake",
     "score_label": "Best",      "icon_color": (60,  180, 80),  "icon": "snake",
     "description": "Eat fruit and grow. Don't hit yourself.",
     "controls": "Arrow keys  |  R to restart  |  ESC to menu"},
    {"name": "Space Asteroids",  "file": "space_asteroids.py",  "score_key": "space_asteroids",
     "score_label": "Best",      "icon_color": (80,  160, 255), "icon": "asteroid",
     "description": "Shoot rotating asteroids before they hit you.",
     "controls": "Left/Right  |  Space to shoot  |  R to restart  |  ESC to menu"},
    {"name": "Space Defenders",  "file": "space_defenders.py",  "score_key": "space_defenders",
     "score_label": "Best",      "icon_color": (160, 80, 255),  "icon": "defender",
     "description": "Waves of enemies. Watch for the boss at 20pts!",
     "controls": "Left/Right  |  Space to shoot  |  R to restart  |  ESC to menu"},
    {"name": "Maze Explorer",    "file": "maze_explorer.py",    "score_key": "maze_explorer",
     "score_label": "Best moves", "icon_color": (255, 160, 40),  "icon": "maze",
     "description": "Navigate a random maze in as few moves as possible.",
     "controls": "Arrow keys  |  R to restart  |  ESC to menu"},
    {"name": "Stack Attack",     "file": "stack_attack.py",     "score_key": "stack_attack",
     "score_label": "Best",      "icon_color": (255,  60, 180), "icon": "stackattack",
     "description": "Stack falling blocks and clear rows. Deep space theme.",
     "controls": "Arrows  |  Space hard drop  |  C hold  |  P pause  |  ESC to menu"},
    {"name": "Hyper Bounce",     "file": "hyper_bounce.py",     "score_key": "hyper_bounce",
     "score_label": "Best",      "icon_color": (0,   160, 255), "icon": "hyperbounce",
     "description": "Smash energy cells with an electric ball. Neon chaos.",
     "controls": "Left/Right  |  Space to launch  |  R to restart  |  ESC to menu"},
    {"name": "Helicopter Dash",  "file": "helicopter_dash.py",  "score_key": "helicopter_dash",
     "score_label": "Best",      "icon_color": (255, 120,   0), "icon": "helicopter",
     "description": "Hold to thrust through a twisting cave. How far can you go?",
     "controls": "Hold Space or click to thrust  |  R to restart  |  ESC to menu"},
    {"name": "Mine Field",       "file": "mine_field.py",      "score_key": "minesweeper_time",
     "score_label": "Best time", "icon_color": (180, 60,  60),  "icon": "mine",
     "description": "Clear the minefield. First click is always safe.",
     "controls": "Left click = reveal  |  Right click = flag  |  R to restart  |  ESC to menu"},
    {"name": "Solitaire",        "file": "solitaire.py",        "score_key": "solitaire",
     "score_label": "Best",      "icon_color": (60,  120, 220), "icon": "cards",
     "description": "Classic Klondike. Build foundations from Ace to King.",
     "controls": "Click to move  |  Double-click to foundation  |  R to restart  |  ESC to menu"},
    {"name": "Spider Solitaire", "file": "spider_solitaire.py", "score_key": "spider_solitaire",
     "score_label": "Best",      "icon_color": (80,  40,  160), "icon": "spider",
     "description": "Build 8 K-to-A runs. Press 1/2/4 for difficulty.",
     "controls": "Click to select/move  |  1/2/4 suits  |  R to restart  |  ESC to menu"},
    {"name": "TriPeaks",         "file": "tripeaks.py",         "score_key": "tripeaks",
     "score_label": "Best",      "icon_color": (40,  160, 100), "icon": "peaks",
     "description": "Clear three peaks playing +/-1 from the waste pile.",
     "controls": "Click free card  |  Click stock to draw  |  R to restart  |  ESC to menu"},
    {"name": "Sudoku",           "file": "sudoku.py",           "score_key": "sudoku",
     "score_label": "Best",      "icon_color": (255,  90,  40), "icon": "sudoku",
     "description": "Fill the grid. Every row, col and box needs 1-9.",
     "controls": "Click cell, type number  |  P pencil  |  E/M/H difficulty  |  ESC to menu"},
    {"name": "Hangman",          "file": "hangman.py",          "score_key": "hangman",
     "score_label": "Best",      "icon_color": (160, 100, 220), "icon": "hangman",
     "description": "Guess the word before the man is hung.",
     "controls": "Type a letter or click keyboard  |  E/M/H difficulty  |  ESC to menu"},
    {"name": "2048",             "file": "game2048.py",         "score_key": "2048",
     "score_label": "Best",      "icon_color": (237, 194, 46),  "icon": "2048",
     "description": "Merge tiles to reach 2048. Simple to learn, hard to master.",
     "controls": "Arrow keys or WASD  |  U undo  |  C keep going  |  ESC to menu"},
]

TILE_W, TILE_H = 170, 155
TILE_PAD       = 10
COLS           = 5
GRID_X         = (WIDTH - (COLS * (TILE_W + TILE_PAD) - TILE_PAD)) // 2
GRID_Y         = 105
INFO_H         = 110
INFO_Y         = HEIGHT - INFO_H

def _restore_menu_after_game():
    """Bring the menu back after a game exits."""
    global screen
    frozen = getattr(sys, "frozen", False)
    started = time.monotonic()
    LOGGER.info("Restoring menu (frozen=%s, pygame init=%s)", frozen, pygame.get_init())

    # Fast path: keep SDL alive (games use display.quit only) and swap back to menu size.
    if pygame.get_init():
        try:
            screen = pygame.display.set_mode((WIDTH, HEIGHT))
            screen.fill(BG_DARK)
            pygame.display.set_caption("Games Collection")
            set_window_icon()
            _init_fonts()
            pygame.event.clear()
            pygame.event.pump()
            pygame.display.flip()
            LOGGER.info("Menu restored (fast) in %.2fs", time.monotonic() - started)
            return
        except pygame.error as exc:
            LOGGER.warning("Fast menu restore failed: %s", exc)

    # Slow path: full teardown then reinit (can take many seconds on macOS).
    try:
        pygame.quit()
    except Exception:
        pass
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(BG_DARK)
    pygame.display.set_caption("Games Collection")
    set_window_icon()
    _init_fonts()
    pygame.event.clear()
    pygame.event.pump()
    pygame.display.flip()
    LOGGER.info("Menu restored (full reinit) in %.2fs", time.monotonic() - started)


def _exec_frozen_game(full_path: str, game_file: str) -> None:
    """Run a game script in-process exactly like the original shipped launcher."""
    with open(full_path, encoding="utf-8") as fh:
        source = fh.read()
    real_exit = sys.exit
    real_quit = pygame.quit

    def _soft_pygame_quit():
        """Tear down the game window without destroying SDL (avoids 15–30s reinit)."""
        try:
            pygame.display.quit()
        except pygame.error:
            pass
        try:
            pygame.mixer.quit()
        except pygame.error:
            pass

    sys.exit = lambda *a: None
    pygame.quit = _soft_pygame_quit
    try:
        exec(
            compile(source, full_path, "exec"),
            {
                "__file__": full_path,
                "__name__": "__main__",
                "__builtins__": __builtins__,
            },
        )
    except SystemExit:
        pass
    except Exception:
        LOGGER.exception("Error in game %s", game_file)
        if sys.platform == "darwin":
            try:
                import subprocess
                subprocess.run(
                    [
                        "osascript", "-e",
                        f'display alert "Could not start {game_file}" message '
                        f'"See games_collection.log in Application Support."',
                    ],
                    check=False,
                )
            except Exception:
                pass
        raise
    finally:
        sys.exit = real_exit
        pygame.quit = real_quit
        try:
            pygame.display.quit()
        except pygame.error:
            pass


def launch_game(game_idx):
    """Launch a game. Packaged: in-process exec (original). Source: subprocess."""
    g = GAMES[game_idx]
    script_dir = get_script_dir()
    full_path = os.path.join(script_dir, g["file"])
    if not os.path.exists(full_path):
        LOGGER.error("File not found: %s (script_dir=%s)", full_path, script_dir)
        return

    frozen = getattr(sys, "frozen", False)
    LOGGER.info("Launching game: %s (%s, frozen=%s)", g["name"], g["file"], frozen)

    if not frozen:
        try:
            pygame.display.iconify()
        except pygame.error as exc:
            LOGGER.warning("Could not iconify menu window: %s", exc)

    try:
        if frozen:
            _exec_frozen_game(full_path, g["file"])
        else:
            launch_game_subprocess(g["file"])
    except Exception:
        LOGGER.exception("Error launching %s", g["file"])
    finally:
        _restore_menu_after_game()

def draw_icon(surf, icon_type, cx, cy, color, size=36):
    if icon_type == "dodge":
        pygame.draw.rect(surf, WHITE, (cx-10, cy+8, 20, 16), border_radius=3)
        pygame.draw.rect(surf, color,  (cx-6,  cy-20, 14, 14), border_radius=2)
    elif icon_type == "snake":
        pts = [(cx-18,cy+8),(cx-10,cy-4),(cx,cy+8),(cx+10,cy-4),(cx+18,cy+8)]
        pygame.draw.lines(surf, color, False, pts, 5)
        pygame.draw.circle(surf, color, (cx+18, cy+8), 6)
        pygame.draw.circle(surf, WHITE, (cx+20, cy+6), 2)
    elif icon_type == "asteroid":
        import math
        pts = [(cx + int(20*math.cos(math.radians(i*72-90))),
                cy + int(20*math.sin(math.radians(i*72-90)))) for i in range(5)]
        pygame.draw.polygon(surf, color, pts, 3)
        pygame.draw.circle(surf, WHITE, (cx-6, cy-6), 3)
    elif icon_type == "defender":
        pygame.draw.polygon(surf, color, [(cx,cy-18),(cx-14,cy+12),(cx,cy+4),(cx+14,cy+12)])
        pygame.draw.rect(surf, GOLD, (cx-2, cy-28, 4, 12))
    elif icon_type == "maze":
        for i in range(3):
            pygame.draw.line(surf, GRAY, (cx-18+i*12, cy-18), (cx-18+i*12, cy+18), 2)
            pygame.draw.line(surf, GRAY, (cx-18, cy-18+i*12), (cx+18, cy-18+i*12), 2)
        pygame.draw.circle(surf, color, (cx-12, cy-12), 5)
        pygame.draw.circle(surf, GOLD,  (cx+12, cy+12), 5)
    elif icon_type == "stackattack":
        block_colors = [(0,210,255),(180,60,230),(255,205,50),(0,210,90)]
        positions = [(cx-18,cy+8),(cx+2,cy+8),(cx-8,cy-6),(cx+12,cy-6)]
        for (bx,by),bc in zip(positions, block_colors):
            pygame.draw.rect(surf, bc, (bx,by,18,16), border_radius=3)
            bright = tuple(min(255,v+70) for v in bc)
            pygame.draw.rect(surf, bright, (bx+2,by+2,14,4), border_radius=1)
    elif icon_type == "hyperbounce":
        # Neon rect cells, glowing ball, electric paddle
        cell_cols = [(255,40,160),(180,30,255),(0,160,255),(0,230,180),
                     (0,220,80),(255,200,0)]
        for i, cc in enumerate(cell_cols):
            rx = cx - 22 + (i%3)*16
            ry = cy - 18 + (i//3)*12
            pygame.draw.rect(surf, cc, (rx,ry,14,8), border_radius=2)
            bright = tuple(min(255,v+90) for v in cc)
            pygame.draw.rect(surf, bright, (rx+2,ry+2,10,3), border_radius=1)
        pygame.draw.circle(surf, (0,220,255), (cx+10, cy+10), 5)
        pygame.draw.circle(surf, WHITE,       (cx+8,  cy+8),  2)
        pygame.draw.rect(surf, (0,200,255), (cx-18, cy+18, 26, 5), border_radius=3)
        bright2 = (100,230,255)
        pygame.draw.rect(surf, bright2, (cx-18, cy+18, 26, 5), 1, border_radius=3)
    elif icon_type == "helicopter":
        pygame.draw.ellipse(surf, color, (cx-22, cy-7, 44, 14))
        pygame.draw.ellipse(surf, WHITE,  (cx+2,  cy-9, 18, 12))
        pygame.draw.line(surf, GRAY, (cx-22, cy-3), (cx-36, cy-2), 2)
        pygame.draw.line(surf, GRAY, (cx-22, cy+3), (cx-36, cy+2), 2)
        pygame.draw.line(surf, WHITE, (cx-32, cy+7), (cx+18, cy+7), 2)
        import math
        for i in range(3):
            a = math.radians(i*120 + pygame.time.get_ticks()//30 % 360)
            pygame.draw.line(surf, GRAY, (cx, cy-10),
                (int(cx+math.cos(a)*26), int(cy-10+math.sin(a)*5)), 2)
    elif icon_type == "mine":
        pygame.draw.circle(surf, color, (cx, cy), 14)
        import math
        for angle in range(0, 360, 45):
            ex = cx + int(20*math.cos(math.radians(angle)))
            ey = cy + int(20*math.sin(math.radians(angle)))
            pygame.draw.line(surf, color, (cx, cy), (ex, ey), 3)
        pygame.draw.circle(surf, WHITE, (cx-4, cy-5), 4)
    elif icon_type == "cards":
        for i, offset in enumerate([-10, -2, 6]):
            r = pygame.Rect(cx+offset-8, cy-14, 22, 30)
            pygame.draw.rect(surf, WHITE if i==2 else LIGHT_GRAY, r, border_radius=2)
            pygame.draw.rect(surf, GRAY, r, 1, border_radius=2)
        suit = small_font.render("♥", True, RED)
        surf.blit(suit, (cx-2, cy-12))
    elif icon_type == "spider":
        import math
        for i in range(6):
            a = math.radians(i*60)
            pygame.draw.line(surf, color, (cx, cy),
                (cx+int(18*math.cos(a)), cy+int(18*math.sin(a))), 1)
        for r2 in [8, 15]:
            pts2 = [(cx+int(r2*math.cos(math.radians(i*60))),
                     cy+int(r2*math.sin(math.radians(i*60)))) for i in range(6)]
            pygame.draw.polygon(surf, color, pts2, 1)
        pygame.draw.circle(surf, color, (cx, cy), 4)
    elif icon_type == "peaks":
        for i, tx in enumerate([cx-16, cx, cx+16]):
            h = 22 - i*4 if i != 1 else 26
            pygame.draw.polygon(surf, color,
                [(tx, cy-h//2+4), (tx-8, cy+14), (tx+8, cy+14)])
    elif icon_type == "sudoku":
        nums = ["1","","3","","5","","7","","9"]
        for i, n in enumerate(nums):
            r2, c2 = i//3, i%3
            rx = cx - 18 + c2*12
            ry = cy - 16 + r2*12
            pygame.draw.rect(surf, (40,40,60), (rx,ry,11,11), border_radius=1)
            if n:
                ns = small_font.render(n, True, color)
                surf.blit(ns, (rx+2, ry))
    elif icon_type == "hangman":
        pygame.draw.line(surf, GALLOWS, (cx-18, cy+18), (cx+4, cy+18), 3)
        pygame.draw.line(surf, GALLOWS, (cx-10, cy-18), (cx-10, cy+18), 3)
        pygame.draw.line(surf, GALLOWS, (cx-10, cy-18), (cx+8, cy-18), 3)
        pygame.draw.line(surf, ROPE,    (cx+8, cy-18), (cx+8, cy-10), 2)
        pygame.draw.circle(surf, color, (cx+8, cy-4), 6, 2)
        pygame.draw.line(surf, color, (cx+8, cy+2),  (cx+8, cy+12), 2)
        pygame.draw.line(surf, color, (cx+8, cy+6),  (cx+2, cy+10), 2)
        pygame.draw.line(surf, color, (cx+8, cy+6),  (cx+14,cy+10), 2)
        pygame.draw.line(surf, color, (cx+8, cy+12), (cx+3, cy+18), 2)
        pygame.draw.line(surf, color, (cx+8, cy+12), (cx+13,cy+18), 2)
    elif icon_type == "2048":
        tile_data = [(2,(238,228,218)),(4,(237,224,200)),(8,(242,177,121)),(16,(245,149,99))]
        for i, (v, tc) in enumerate(tile_data):
            rx = cx - 20 + (i%2)*22
            ry = cy - 20 + (i//2)*22
            pygame.draw.rect(surf, tc, (rx, ry, 18, 18), border_radius=3)
            ns = small_font.render(str(v), True,
                (119,110,101) if v<=4 else (249,246,242))
            surf.blit(ns, ns.get_rect(center=(rx+9, ry+9)))


def draw_tile(surf, game_idx, tx, ty, hovered, scores):
    g = GAMES[game_idx]
    color = g["icon_color"]
    if hovered:
        pygame.draw.rect(surf, (35, 42, 75), (tx, ty, TILE_W, TILE_H), border_radius=14)
        pygame.draw.rect(surf, color, (tx, ty, TILE_W, TILE_H), 2, border_radius=14)
    else:
        pygame.draw.rect(surf, BG_PANEL, (tx, ty, TILE_W, TILE_H), border_radius=14)
        pygame.draw.rect(surf, (40, 45, 70), (tx, ty, TILE_W, TILE_H), 1, border_radius=14)
    icon_bg = (max(0,color[0]-60), max(0,color[1]-60), max(0,color[2]-60))
    pygame.draw.rect(surf, icon_bg, (tx+8, ty+8, TILE_W-16, 76), border_radius=10)
    draw_icon(surf, g["icon"], tx + TILE_W//2, ty + 46, color)
    name_s = menu_font.render(g["name"], True, WHITE if hovered else LIGHT_GRAY)
    surf.blit(name_s, name_s.get_rect(centerx=tx+TILE_W//2, y=ty+88))
    key = g.get("score_key")
    val = scores.get(key) if key else None
    if val is not None:
        label = g["score_label"]
        val_str = (f"{label}: {float(val):.0f}s" if "time" in label.lower()
                   else f"{label}: {int(val)}")
        sc_s = small_font.render(val_str, True, GOLD)
        surf.blit(sc_s, sc_s.get_rect(centerx=tx+TILE_W//2, y=ty+110))
    else:
        no_s = small_font.render("No score yet", True, GRAY)
        surf.blit(no_s, no_s.get_rect(centerx=tx+TILE_W//2, y=ty+110))
    if hovered:
        # Draw a solid triangle instead of relying on a Unicode glyph
        label_s = info_font.render("Play", True, color)
        label_x = tx + TILE_W//2 - label_s.get_width()//2 + 10
        surf.blit(label_s, (label_x, ty+134))
        # Triangle to the left of the text
        tri_x = label_x - 14
        tri_y = ty + 134 + label_s.get_height()//2
        pygame.draw.polygon(surf, color, [
            (tri_x,     tri_y - 6),
            (tri_x,     tri_y + 6),
            (tri_x + 10, tri_y),
        ])


def draw_info_bar(surf, game_idx):
    pygame.draw.rect(surf, BG_PANEL, (0, INFO_Y, WIDTH, INFO_H))
    pygame.draw.line(surf, ACCENT, (0, INFO_Y), (WIDTH, INFO_Y), 1)
    if game_idx is None:
        hint = info_font.render(
            "Hover a game to see details  —  click to play  —  ESC to quit", True, GRAY)
        surf.blit(hint, hint.get_rect(center=(WIDTH//2, INFO_Y + INFO_H//2)))
        return
    g = GAMES[game_idx]
    name_s = title_font.render(g["name"], True, WHITE)
    surf.blit(name_s, (30, INFO_Y + 12))
    desc_s = info_font.render(g["description"], True, LIGHT_GRAY)
    surf.blit(desc_s, (30, INFO_Y + 78))
    ctrl_lbl = small_font.render("CONTROLS", True, ACCENT)
    surf.blit(ctrl_lbl, (WIDTH - 420, INFO_Y + 14))
    ctrl_s = info_font.render(g["controls"], True, LIGHT_GRAY)
    surf.blit(ctrl_s, (WIDTH - 420, INFO_Y + 34))


def main():
    global screen
    scores        = get_all_scores()
    score_refresh = time.time()
    hovered_idx     = None
    return_cooldown = 0   # frames to ignore clicks after returning from a game
    clock           = pygame.time.Clock()
    running         = True

    while running:
        clock.tick(60)
        if return_cooldown > 0:
            return_cooldown -= 1
        mouse = pygame.mouse.get_pos()

        if time.time() - score_refresh > 2:
            scores = get_all_scores()
            score_refresh = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if hovered_idx is not None and return_cooldown == 0:
                    launch_game(hovered_idx)
                    hovered_idx     = None
                    return_cooldown = 20   # ignore clicks for ~0.3s after returning
                    scores = get_all_scores()

        hovered_idx = None
        for i in range(len(GAMES)):
            row, col = divmod(i, COLS)
            tx = GRID_X + col * (TILE_W + TILE_PAD)
            ty = GRID_Y + row * (TILE_H + TILE_PAD)
            if pygame.Rect(tx, ty, TILE_W, TILE_H).collidepoint(mouse):
                hovered_idx = i
                break

        screen.fill(BG_DARK)
        for gx in range(0, WIDTH, 30):
            for gy in range(0, HEIGHT, 30):
                pygame.draw.circle(screen, (25, 28, 50), (gx, gy), 1)
        pygame.draw.rect(screen, BG_PANEL, (0, 0, WIDTH, 95))
        pygame.draw.line(screen, ACCENT, (0, 95), (WIDTH, 95), 1)
        title_s = title_font.render("Games Collection", True, WHITE)
        screen.blit(title_s, (30, 22))
        esc_s = small_font.render("ESC to quit", True, GRAY)
        screen.blit(esc_s, (WIDTH - esc_s.get_width() - 20, 38))
        for i in range(len(GAMES)):
            row, col = divmod(i, COLS)
            tx = GRID_X + col * (TILE_W + TILE_PAD)
            ty = GRID_Y + row * (TILE_H + TILE_PAD)
            draw_tile(screen, i, tx, ty, hovered_idx == i, scores)
        draw_info_bar(screen, hovered_idx)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
