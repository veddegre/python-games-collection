import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import json
import os

SCORES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scores.json")

def load_scores():
    if os.path.exists(SCORES_FILE):
        try:
            with open(SCORES_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def get_high_score(game_name):
    scores = load_scores()
    return scores.get(game_name, 0)

def save_high_score(game_name, score):
    scores = load_scores()
    if score > scores.get(game_name, 0):
        scores[game_name] = score
        try:
            with open(SCORES_FILE, "w") as f:
                json.dump(scores, f, indent=2)
            return True  # New high score!
        except Exception:
            pass
    return False

def get_all_scores():
    return load_scores()
