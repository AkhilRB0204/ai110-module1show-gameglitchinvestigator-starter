from logic_utils import check_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"


# Regression tests for the bugs fixed in Phase 2 (generated with Claude Code).
from logic_utils import OUTCOME_MESSAGES


def test_guess_too_high_hint_says_lower():
    # Bug: a guess of 60 vs secret 50 told the player to go HIGHER.
    outcome = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in OUTCOME_MESSAGES[outcome]


def test_guess_too_low_hint_says_higher():
    outcome = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in OUTCOME_MESSAGES[outcome]


def test_small_guess_is_too_low_not_too_high():
    # Bug: on even attempts the secret became "50", and "9" > "50" as strings.
    assert check_guess(9, 50) == "Too Low"
