import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import json
import logging

from game_runtime import migrate_legacy_scores_if_needed, scores_path

LOGGER = logging.getLogger("games_collection.highscores")

def load_scores():
    migrate_legacy_scores_if_needed()
    scores_file = scores_path()
    if os.path.exists(scores_file):
        try:
            with open(scores_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError) as exc:
            LOGGER.warning("Could not read scores file %s: %s", scores_file, exc)
    return {}

def get_high_score(game_name):
    scores = load_scores()
    return scores.get(game_name, 0)

def save_high_score(game_name, score):
    scores = load_scores()
    if score > scores.get(game_name, 0):
        scores[game_name] = score
        try:
            with open(scores_path(), "w", encoding="utf-8") as f:
                json.dump(scores, f, indent=2)
            return True  # New high score!
        except OSError as exc:
            LOGGER.error("Failed to save high score for %s to %s: %s", game_name, scores_path(), exc)
    return False

def get_all_scores():
    return load_scores()
