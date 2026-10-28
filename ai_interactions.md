# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I used Claude Code (in VS Code) to do both optional challenges in one go: add 5 new song features to the dataset and make the scoring use them (Challenge 1), and add different scoring modes that I can switch between from `main.py` (Challenge 2). It had to change the CSV, the scoring code, and the runner, and then check that nothing I already documented broke.

**Prompts used:**

> "Challenge 1: Add Advanced Song Features. Introduce 5 or more complex attributes to your dataset that are not currently present in the baseline data, such as Song Popularity (0-100), Release Decade, or Detailed Mood Tags (e.g., "nostalgic," "aggressive," "euphoric"). Update both data/songs.csv and the scoring logic in src/recommender.py so scoring accounts for the new attributes."

> "Challenge 2: Create Multiple Scoring Modes. Build two or more different ranking strategies (e.g., "Genre-First," "Mood-First," or "Energy-Focused") so a user can switch between modes in main.py. Brainstorm a design pattern (like a simple "Strategy" pattern) that keeps your code modular."

**What did the agent generate or change?**

- **`data/songs.csv`:** added 5 new columns for all 20 songs:
  - `popularity` (0 to 100): how well-known the song is
  - `release_decade` (like 1990 or 2020)
  - `mood_tags`: 3 detailed tags per song, like `aggressive;intense;dark` or `nostalgic;warm;carefree`
  - `liveness` (0 to 1): how much it sounds like a live recording
  - `speechiness` (0 to 1): how much rapping or talking is in it
- **`src/recommender.py`:**
  - `load_songs` now turns the new number columns into ints and floats, and splits `mood_tags` into a list.
  - `score_song` gives points for the new features, but **only if the user sets that preference**:

    | Preference | Points |
    |---|---|
    | `wanted_tags` | +0.5 per shared mood tag (counts up to 2 tags) |
    | `target_popularity` | up to +0.5, more the closer the song is (the gap is divided by 100 so it stays 0 to 1) |
    | `favorite_decade` | +0.5 for the same decade, +0.25 for one decade off |
    | `likes_live` | +0.5 if the song is live (liveness 0.5 or higher) and you want live, or neither |
    | `likes_rap` | +0.5 if the song has a lot of rapping (speechiness 0.33 or higher) and you want that, or neither |

  - Added a `max_score()` function, because the best possible score now depends on which preferences the user set (5.0 for basic profiles, 8.0 when all the advanced ones are set).
  - Added the new fields to `Song` and `UserProfile` with defaults, so the starter tests still work.
- **`src/main.py`:** added two new profiles that use the advanced features ("Rock with Mood Tags" and "Nostalgic Hidden Gems"). The header now shows the advanced settings, and each score is shown out of that profile's real max.

**What did you verify or fix manually?**

The agent ran these checks and I went over the results:

- **Nothing old broke.** It saved the output before making changes and compared it after. The 8 original profiles gave the exact same songs, scores, and reasons, because they don't set any of the new preferences. The only new lines were the scoring mode line and the 2 new profiles.
- **The math stays valid.** For every profile in every mode, every song's score stayed between 0 and that profile's max score, and the points in the reasons always added up to the total. (The Energy Too High edge case was left out of this check because it's already known to go negative.)
- **Both starter tests still pass.**
- **A bug it caught:** the first version of the "close decade" reason had a comma in it ("close decade, 2010s"). `main.py` splits the reasons on commas, so it printed as two broken bullet points. It got changed to "close decade: 2010s".
- **Did it actually help?** In the "Rock with Mood Tags" profile, Iron Tempest (metal) jumped from #4 to #2, right behind Storm Runner. Its tags (aggressive, intense, dark) finally let the system see that metal fits a rock fan, which partly fixes the "metal doesn't count as rock" problem from my model card.
- **One thing to keep in mind:** all the new values (popularity, decade, tags, etc.) are made up, just like the original songs.

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

The **Strategy pattern**. Each scoring mode is a "strategy": an object with the same shape that the scoring function can use. The program picks one when it starts, and the scoring code doesn't need to know which one it got.

**How did AI help you brainstorm or implement it?**

I asked Claude to brainstorm a design pattern that would keep the code modular. It came up with three options:

1. **An if/else on the mode name inside `score_song`** (like `if mode == "mood-first": ...`). This is the quickest to write, but every new mode makes `score_song` longer and messier, and it mixes "how to score" with "which mode is on."
2. **A full Strategy with a class for each mode**, each with its own `score()` method. This is the textbook version, but all my modes use the same scoring steps and only change how much each one counts, so it would mean copying the same code four times.
3. **A data-driven Strategy:** one small `ScoringStrategy` object that just holds the weights, plus a dictionary of named modes. `score_song` takes whichever strategy it's given and uses its weights.

I went with option 3, because my modes really only differ in their weights. Adding a new mode is one line, and `score_song` didn't need any if/else for modes. The AI also suggested making the strategies `frozen` so a mode's weights can't get changed by accident while the program runs.

**How does the pattern appear in your final code?**

- `ScoringStrategy` in `src/recommender.py` is the strategy. It holds one weight per feature, plus a name and a description.
- There are four modes, all collected in the `STRATEGIES` dictionary:

  | Mode | What it does |
  |---|---|
  | `BALANCED` | The original recipe (genre 2.0, mood 1.0, energy 1.0) |
  | `GENRE_FIRST` | Genre 3.0, mood 0.5, energy 0.5 |
  | `MOOD_FIRST` | Genre 0.5, mood 2.5, and mood tags count double |
  | `ENERGY_FOCUSED` | Genre 1.0, mood 0.5, energy 3.0 |

- `score_song(user_prefs, song, strategy)`, `recommend_songs(..., strategy)`, `max_score(user_prefs, strategy)` and the `Recommender` class all take a strategy, and default to `BALANCED`.
- In `src/main.py`, you switch modes with `python -m src.main --mode mood-first` (or `balanced`, `genre-first`, `energy-focused`).

**What the modes changed:**

- **Sad but Hyped:** in Energy-Focused mode, the calm sad folk song drops out completely and the list is all loud songs. That's the "hyped" side winning instead of the "sad" side.
- **Acoustic Headbanger:** Energy-Focused finally gives this person only loud songs. Genre-First makes it worse, with 4 calm study songs in the top 5, because lowering the energy weight lets the acoustic and instrumental bonuses take over.
- **Pop / Happy:** Mood-First moves Rooftop Lights (happy) above Gym Hero (intense).
- **Profiles with one obvious best match** (like Deep Intense Rock) gave the same top 5 in every mode.
