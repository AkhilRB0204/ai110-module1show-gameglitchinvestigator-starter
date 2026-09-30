from logic_utils import (
    check_guess,
    get_attempt_limit,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)


def test_numeric_not_lexicographic_comparison():
    # "9" > "50" as strings; as numbers 9 is too low.
    assert check_guess(9, 50) == "Too Low"
    assert check_guess(100, 50) == "Too High"


def test_difficulty_gets_harder():
    easy, normal, hard = (get_range_for_difficulty(d)[1] for d in ("Easy", "Normal", "Hard"))
    assert easy < normal < hard
    assert get_attempt_limit("Easy") > get_attempt_limit("Normal") > get_attempt_limit("Hard")


def test_parse_guess_validation():
    assert parse_guess("42", 1, 100) == (True, 42, None)
    assert parse_guess(" 7 ", 1, 20) == (True, 7, None)
    assert parse_guess("", 1, 100)[0] is False
    assert parse_guess("abc", 1, 100)[0] is False
    assert parse_guess("3.9", 1, 100)[0] is False
    assert parse_guess("500", 1, 100)[0] is False
    assert parse_guess("0", 1, 100)[0] is False


def test_scoring():
    assert update_score(0, "Win", 1) == 100
    assert update_score(0, "Win", 3) == 80
    assert update_score(0, "Win", 50) == 10
    for attempt in (1, 2, 3, 4):
        assert update_score(0, "Too High", attempt) == -5
        assert update_score(0, "Too Low", attempt) == -5
