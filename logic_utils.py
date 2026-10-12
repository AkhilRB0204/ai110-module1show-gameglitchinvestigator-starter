# FIX: Hard was 1-50 (smaller than Normal) and Easy had fewer attempts than Normal.
# Claude Code moved the settings here so each difficulty scales properly; verified by test_difficulty_gets_harder.
DIFFICULTY_SETTINGS = {
    # difficulty: (low, high, attempt_limit)
    "Easy": (1, 20, 8),
    "Normal": (1, 100, 7),
    "Hard": (1, 200, 6),
}

# FIX: The starter hints were backwards ("Too High" said "Go HIGHER!").
# Claude Code swapped them and moved them out of check_guess; verified with test_guess_too_high_hint_says_lower.
OUTCOME_MESSAGES = {
    "Win": "🎉 Correct!",
    "Too High": "📉 Too high — go LOWER!",
    "Too Low": "📈 Too low — go HIGHER!",
}


def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    low, high, _ = DIFFICULTY_SETTINGS.get(difficulty, DIFFICULTY_SETTINGS["Normal"])
    return low, high


def get_attempt_limit(difficulty: str):
    """Return the number of guesses allowed for a given difficulty."""
    _, _, limit = DIFFICULTY_SETTINGS.get(difficulty, DIFFICULTY_SETTINGS["Normal"])
    return limit


def parse_guess(raw: str, low: int = None, high: int = None):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None or raw.strip() == "":
        return False, None, "Enter a guess."

    # FIX: "3.9" used to be truncated to 3 and out-of-range guesses were accepted.
    # Refactored from app.py into logic_utils.py with Claude Code, then added a range check.
    try:
        value = int(raw.strip())
    except ValueError:
        return False, None, "That is not a whole number."

    if low is not None and high is not None and not (low <= value <= high):
        return False, None, f"Guess must be between {low} and {high}."

    return True, value, None


def check_guess(guess: int, secret: int):
    """
    Compare guess to secret and return the outcome.

    outcome examples: "Win", "Too High", "Too Low"
    """
    # FIX: The starter compared the secret as a string on even attempts ("9" > "50").
    # Claude Code refactored this into logic_utils.py and removed the str fallback so comparison is always numeric.
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number (1 = first guess)."""
    # FIX: Win bonus used attempt_number + 1 (off by one) and "Too High" gave +5 on even attempts.
    # Fixed with Claude Code; test_scoring checks both.
    if outcome == "Win":
        points = 100 - 10 * (attempt_number - 1)
        return current_score + max(points, 10)

    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    return current_score
