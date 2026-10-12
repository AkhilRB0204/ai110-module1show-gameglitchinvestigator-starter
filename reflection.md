# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

The game loaded fine and looked normal. It had a title, a difficulty picker in the sidebar, a text box, and Submit / New Game buttons. It broke as soon as I played. The hints sent me the wrong way, the info box always said "between 1 and 100" whatever the difficulty, and my score sometimes went up after a wrong guess. Once I won or lost, clicking **New Game** didn't let me play again. None of this caused a crash or an error message, so the bugs were easy to miss unless I watched the game closely.

Concrete bugs I found (line numbers are from the original starter `app.py`):

1. **The hints were backwards.** Trigger: guess `60` when the secret is 50. Expected: "Too high, go lower." Actual: "📈 Go HIGHER!" Cause: in `check_guess()` (`app.py` lines 32–47), the messages for "Too High" and "Too Low" were swapped.
2. **The secret turned into a string on every second guess.** Trigger: guess `9` on attempt 2 when the secret is 50. Expected: "Too Low." Actual: "Too High." Cause: `app.py` lines 158–161 convert the secret to `str` when `attempts % 2 == 0`. The `except TypeError` fallback in `check_guess()` then compares the two values as text, and `"9" > "50"` is true for strings.
3. **New Game couldn't start a new game.** Trigger: win or lose, then click New Game. Expected: a fresh, playable game. Actual: it kept showing "You already won" / "Game over". Cause: the `new_game` block (`app.py` lines 134–138) never reset `status`, so `st.stop()` on line 145 ran on every rerun. It also always used `random.randint(1, 100)` instead of the range for the chosen difficulty.
4. **The difficulty settings didn't scale.** Hard used 1–50, a smaller range than Normal's 1–100 (`get_range_for_difficulty()`, lines 4–11). Easy got fewer attempts than Normal (`attempt_limit_map`, lines 80–84).
5. **Scoring and attempt counting were off.** `attempts` started at 1 (line 96), so one guess was gone before I played. Invalid input still used up an attempt (line 148). `update_score()` gave +5 for a "Too High" guess on even attempts (line 58), and the win bonus used `attempt_number + 1` (line 52), so a first-guess win scored 80 instead of 100.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error | Suspected Code Location |
|-------|-------------------|-----------------|------------------------|-------------------------|
| Guess `60` when the secret is 50 | The hint says the guess is too high, so go lower | Says "📈 Go HIGHER!" (the hints are backwards) | No error; `check_guess(60, 50)` returns `('Too High', '📈 Go HIGHER!')` | `check_guess()`, `app.py` lines 32–47 |
| Guess `9` on the 2nd attempt when the secret is 50 | "Too Low" | "Too High", because on even attempts the secret becomes the string `"50"` and `"9" > "50"` compares as text | No error; the `TypeError` is caught silently and the code falls back to comparing strings | `app.py` lines 158–161 (`attempts % 2 == 0`) and the `except TypeError` branch of `check_guess()` |
| Win or lose a game, then click **New Game** | A fresh game starts | Still shows "You already won" / "Game over" and the game can't be played; the new secret is also picked from 1–100 even on Easy | No error; `status` is never reset, so `st.stop()` runs on every rerun | `new_game` block, `app.py` lines 134–138; `st.stop()` on line 145 |
| Choose **Hard** difficulty | A bigger range than Normal | The range is 1–50, smaller than Normal's 1–100 | No error | `get_range_for_difficulty()`, `app.py` lines 4–11 |
| Guess `3.9` | Rejected, because guesses should be whole numbers | Accepted as `3` and uses up an attempt | No error | `parse_guess()`, `app.py` line 23 (`int(float(raw))`) |
| Guess `150` on Normal (range 1–100) | Rejected as out of range | Accepted and uses up an attempt | No error | `parse_guess()` has no range check, `app.py` lines 14–29 |
| Run `pytest` on the starter code | Tests pass | All 3 tests fail | `NotImplementedError: Refactor this function from app.py into logic_utils.py` | `logic_utils.py`, where every function was a stub |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)? Claude Code
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

I used Claude Code in agent mode inside VS Code. Rather than suggesting changes for me to type in, it edited `app.py` and `logic_utils.py` directly, so my job was to review the diff and check the results.

**Correct suggestion:** Claude Code moved `check_guess()` into `logic_utils.py`, swapped the backwards hint messages, and removed the code that turned the secret into a string on even attempts. That was correct because the original bug had two causes. The messages were swapped, and comparing `"9"` to `"50"` as text gave the wrong answer. Fixing only the messages would have left the second bug in place. I checked it with pytest (`check_guess(60, 50)` returns `"Too High"` with a "go LOWER" hint, and `check_guess(9, 50)` returns `"Too Low"`), and by playing the game and guessing above and below the secret.

**Suggestion not accepted as written:** In this project I didn't reject or rewrite any of the AI's code changes; I accepted them after reviewing the diffs and running the tests. Looking back, that is the part of my process I would change. Claude Code made a lot of changes in one commit (refactor, 10+ bug fixes, new tests), and accepting it all at once made each change harder to review carefully. Next time I would ask for one bug fix at a time, as the assignment suggests, so I can judge each diff on its own and push back on anything that is out of scope.
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I counted a bug as fixed only after two checks passed: a pytest test that reproduces the original trigger, and a manual run in the live game showing the right behavior. The tests alone weren't enough, because some bugs (like New Game not resetting) only show up in the Streamlit UI and its session state. Before the fix, `pytest` failed all 3 starter tests with `NotImplementedError`, because `logic_utils.py` was only stubs. After the refactor and fixes, `pytest -v` passes all 10 tests in `tests/test_game_logic.py` and `tests/test_logic_fixes.py`.

One test was `test_guess_too_high_hint_says_lower`. It checks that a guess of 60 against a secret of 50 returns `"Too High"` and that the hint shown tells the player to go **LOWER**. The original starter test only checked the outcome label. That label was already right in the buggy code, so the test would have missed the backwards message. Another test, `test_small_guess_is_too_low_not_too_high`, checks that 9 vs. 50 is `"Too Low"`, which catches the bug where `"9" > "50"` was compared as strings. In the live game, guessing one above the secret showed "📉 Too high — go LOWER!", typing `abc` showed an error without using up an attempt, and clicking New Game after a win reset the status to playing with 0 attempts and a score of 0.

Claude Code wrote the regression tests. The useful part was that it aimed each test at the exact input that triggered the bug (60 vs. 50, 9 vs. 50, `"3.9"`, `"500"`), instead of writing general happy-path tests. It also pointed out that testing only the outcome label wasn't enough for the backwards-hint bug, which is why the new test checks the message text too.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Streamlit reruns your whole Python script from top to bottom every time the user does anything: clicks a button, types in a box, or changes a dropdown. So an ordinary variable like `secret = random.randint(1, 100)` gets a brand-new value on every click, as if the program had restarted. `st.session_state` is a dictionary that survives those reruns, so anything that has to be remembered between clicks (the secret, the attempts, the score, whether the game is over) has to live there. Several bugs in this game were really state bugs. New Game reset some values in `session_state` but not `status`, so the old "game over" kept coming back. Changing difficulty didn't touch `session_state` at all, so the old secret stayed. Putting every reset in one `start_new_game()` function made it much easier to see what the game remembers.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

The habit I want to keep is writing a regression test for each bug using the exact input that triggered it (like a guess of 60 against a secret of 50), and then also checking the fix in the running app. The original starter test only checked the "Too High" label, and that label was already correct, so it would have passed even though the hint message was still backwards. Next time I would ask the AI for one fix at a time, in separate commits, instead of letting it change everything at once. That way I can actually review each diff and push back when something is out of scope. This project showed me that AI-generated code can look clean and run without errors and still be wrong in ways you only catch by playing it and testing edge cases, so I now treat AI output as a draft to verify, not a finished product.
