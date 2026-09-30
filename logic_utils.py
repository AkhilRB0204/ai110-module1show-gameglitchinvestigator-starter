DIFFICULTY_SETTINGS = {
    # difficulty: (low, high, attempt_limit)
    "Easy": (1, 20, 8),
    "Normal": (1, 100, 7),
    "Hard": (1, 200, 6),
}

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
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number (1 = first guess)."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number - 1)
        return current_score + max(points, 10)

    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    return current_score
