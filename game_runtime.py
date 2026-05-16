"""
Game launch utilities: subprocess isolation, logging, and portable data paths.
"""
from __future__ import annotations

import logging
import os
import shutil
import subprocess
import sys
import time
from typing import Optional

LOGGER = logging.getLogger("games_collection")

GAME_ARG = "--game"


def get_script_dir() -> str:
    if getattr(sys, "frozen", False):
        return sys._MEIPASS  # type: ignore[attr-defined]
    return os.path.dirname(os.path.abspath(__file__))


def get_user_data_dir() -> str:
    name = "GamesCollection"
    if sys.platform == "darwin":
        base = os.path.join(
            os.path.expanduser("~"), "Library", "Application Support", name
        )
    elif sys.platform == "win32":
        base = os.path.join(
            os.environ.get("LOCALAPPDATA", os.path.expanduser("~")), name
        )
    else:
        base = os.path.join(os.path.expanduser("~"), ".config", name)
    os.makedirs(base, exist_ok=True)
    return base


def setup_logging() -> logging.Logger:
    log_path = os.path.join(get_user_data_dir(), "games_collection.log")
    root = logging.getLogger("games_collection")
    if root.handlers:
        return root
    root.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    fh = logging.FileHandler(log_path, encoding="utf-8")
    fh.setFormatter(fmt)
    root.addHandler(fh)
    if not getattr(sys, "frozen", False):
        sh = logging.StreamHandler()
        sh.setFormatter(fmt)
        root.addHandler(sh)
    root.info(
        "Logging started (frozen=%s, platform=%s, executable=%s)",
        getattr(sys, "frozen", False),
        sys.platform,
        sys.executable,
    )
    return root


def game_file_from_argv(argv: Optional[list[str]] = None) -> Optional[str]:
    argv = argv if argv is not None else sys.argv
    for i, arg in enumerate(argv):
        if arg == GAME_ARG and i + 1 < len(argv):
            return argv[i + 1]
    return None


def resolve_game_path(game_file: str, script_dir: Optional[str] = None) -> Optional[str]:
    """
    Resolve a game filename to an absolute path inside script_dir only.
    Rejects path traversal, absolute paths, and non-.py names.
    """
    script_dir = script_dir or get_script_dir()
    if not game_file or os.path.isabs(game_file):
        LOGGER.error("Rejected game path (absolute or empty): %r", game_file)
        return None
    normalized = game_file.replace("\\", "/")
    if normalized != os.path.basename(normalized):
        LOGGER.error("Rejected game path (not a bare filename): %r", game_file)
        return None
    if not normalized.endswith(".py"):
        LOGGER.error("Rejected game path (not a .py file): %r", game_file)
        return None

    root = os.path.realpath(script_dir)
    full_path = os.path.realpath(os.path.join(root, normalized))
    if not full_path.startswith(root + os.sep):
        LOGGER.error("Rejected game path (outside app directory): %r", game_file)
        return None
    if not os.path.isfile(full_path):
        LOGGER.error("Game file not found: %s", full_path)
        return None
    return full_path


def run_game_in_current_process(game_file: str, script_dir: Optional[str] = None) -> int:
    """Run a game script in this process (used only inside a dedicated child process)."""
    script_dir = script_dir or get_script_dir()
    full_path = resolve_game_path(game_file, script_dir)
    if not full_path:
        return 1

    LOGGER.info("Starting game in-process: %s", full_path)
    real_exit = sys.exit

    def _blocked_exit(code=0):
        raise SystemExit(code)

    sys.exit = _blocked_exit
    started = time.monotonic()
    try:
        with open(full_path, encoding="utf-8") as fh:
            source = fh.read()
        namespace = {
            "__file__": full_path,
            "__name__": "__main__",
            "__builtins__": __builtins__,
        }
        exec(compile(source, full_path, "exec"), namespace)
        LOGGER.info("Game finished normally: %s (%.2fs)", game_file, time.monotonic() - started)
        return 0
    except SystemExit as exc:
        code = exc.code if exc.code is not None else 0
        LOGGER.info(
            "Game exited: %s code=%s (%.2fs)", game_file, code, time.monotonic() - started
        )
        return int(code) if isinstance(code, int) else 0
    except Exception:
        LOGGER.exception("Game crashed: %s (%.2fs)", game_file, time.monotonic() - started)
        return 1
    finally:
        sys.exit = real_exit


def _subprocess_launch_cmd(game_file: str) -> list[str]:
    if getattr(sys, "frozen", False):
        return [sys.executable, GAME_ARG, game_file]
    menu_py = os.path.join(get_script_dir(), "menu.py")
    return [sys.executable, "-B", menu_py, GAME_ARG, game_file]


def launch_game_subprocess(game_file: str, script_dir: Optional[str] = None) -> int:
    """Launch a game in a child process (works for source and PyInstaller builds)."""
    script_dir = script_dir or get_script_dir()
    if not resolve_game_path(game_file, script_dir):
        return 1

    cmd = _subprocess_launch_cmd(game_file)
    LOGGER.info("Launching subprocess: %s (cwd=%s)", cmd, script_dir)
    started = time.monotonic()
    try:
        result = subprocess.run(
            cmd,
            cwd=script_dir,
            check=False,
        )
        elapsed = time.monotonic() - started
        LOGGER.info(
            "Subprocess finished: %s returncode=%s (%.2fs)",
            game_file,
            result.returncode,
            elapsed,
        )
        return result.returncode
    except Exception:
        LOGGER.exception("Failed to launch subprocess for %s", game_file)
        return 1


def handle_subprocess_game_argv() -> bool:
    """
    If this process was started as a game child (--game <file>), run that game and
  return True so the caller can exit without starting the menu.
    """
    setup_logging()
    game_file = game_file_from_argv()
    if not game_file:
        return False
    code = run_game_in_current_process(game_file)
    sys.exit(code)


def legacy_scores_path() -> str:
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "scores.json")


def scores_path() -> str:
    return os.path.join(get_user_data_dir(), "scores.json")


def migrate_legacy_scores_if_needed() -> None:
    user_path = scores_path()
    legacy = legacy_scores_path()
    if os.path.exists(user_path) or not os.path.exists(legacy):
        return
    try:
        shutil.copy2(legacy, user_path)
        LOGGER.info("Migrated scores from %s to %s", legacy, user_path)
    except OSError as exc:
        LOGGER.warning("Could not migrate scores: %s", exc)
