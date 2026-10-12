# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] **The game's purpose:** a Streamlit number-guessing game. The player picks a difficulty (Easy 1–20, Normal 1–100, Hard 1–200), then guesses a secret number. After each guess they get a "too high" or "too low" hint, and their score depends on how quickly they win before running out of attempts.
- [x] **Bugs I found:**
  - The hints were backwards ("Too High" said "Go HIGHER!").
  - On every second guess the secret was compared as text, so `9` counted as higher than `50`.
  - New Game didn't reset the win/loss status, so you couldn't play again. It also ignored the difficulty's range.
  - The difficulties didn't scale: Hard (1–50) had a smaller range than Normal, and Easy got fewer attempts.
  - The attempt counter started at 1, and invalid input still used up a guess.
  - Decimal guesses and guesses outside the range were accepted.
  - Scoring was wrong: some wrong guesses added +5, and the win bonus was off by one.
  - The info box always said "1 to 100", and "attempts left" lagged one guess behind.
- [x] **Fixes I applied:**
  - Moved all game logic (`check_guess`, `parse_guess`, `update_score`, and the difficulty settings) from `app.py` into `logic_utils.py`.
  - Fixed the hint messages and made sure guesses are always compared as numbers.
  - Added a `start_new_game()` function so first load, New Game, and changing difficulty all fully reset the game.
  - `parse_guess` now accepts only whole numbers within the range, and only valid guesses count as attempts.
  - Corrected the scoring.
  - Added regression tests in `tests/` for each of these bugs.

## 📸 Demo Walkthrough

A sample game on **Normal** difficulty (range 1–100, 7 attempts) where the secret is 55:

1. The game starts. The info box says "Guess a number between 1 and 100. Attempts left: 7", and the score is 0.
2. The user enters `abc`. The game shows "That is not a whole number." Attempts left stays at 7.
3. The user enters a guess of `40`. The game shows "📈 Too low — go HIGHER!". The score drops to -5, and attempts left is 6.
4. The user enters a guess of `70`. The game shows "📉 Too high — go LOWER!". The score drops to -10, and attempts left is 5.
5. The user enters `55`. The game shows "🎉 Correct!" with balloons and "You won! The secret was 55. Final score: 70". That's the -10 so far plus a 90-point win bonus for winning on the 3rd guess.
6. The user tries another guess. The game says "You already won. Start a new game to play again." and the score stays at 70.
7. The user clicks **New Game 🔁**. The game shows "New game started." and resets to attempts left 7 and score 0, with a new secret.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
$ pytest tests/ -v
collecting ... collected 10 items

tests/test_game_logic.py::test_winning_guess PASSED                      [ 10%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 20%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 30%]
tests/test_game_logic.py::test_guess_too_high_hint_says_lower PASSED     [ 40%]
tests/test_game_logic.py::test_guess_too_low_hint_says_higher PASSED     [ 50%]
tests/test_game_logic.py::test_small_guess_is_too_low_not_too_high PASSED [ 60%]
tests/test_logic_fixes.py::test_numeric_not_lexicographic_comparison PASSED [ 70%]
tests/test_logic_fixes.py::test_difficulty_gets_harder PASSED            [ 80%]
tests/test_logic_fixes.py::test_parse_guess_validation PASSED            [ 90%]
tests/test_logic_fixes.py::test_scoring PASSED                           [100%]

============================== 10 passed in 0.01s ==============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
