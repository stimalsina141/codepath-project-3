"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import argparse

from src.recommender import load_songs, recommend_songs, max_score, STRATEGIES

# Default profile: someone who wants upbeat, happy pop with vocals
POP_HAPPY = {
    "favorite_genre": "pop",
    "favorite_mood": "happy",
    "target_energy": 0.80,
    "likes_acoustic": False,
    "likes_instrumental": False,
}

# A "study session" listener who wants calm lofi with no singing
STUDY_SESSION = {
    "favorite_genre": "lofi",
    "favorite_mood": "chill",
    "target_energy": 0.40,
    "likes_acoustic": True,
    "likes_instrumental": True,
}

# Someone who wants loud, aggressive rock with vocals
DEEP_INTENSE_ROCK = {
    "favorite_genre": "rock",
    "favorite_mood": "intense",
    "target_energy": 0.90,
    "likes_acoustic": False,
    "likes_instrumental": False,
}

# --- Edge case profiles: trying to trick the scoring ---

# Conflict: wants sad songs but very high energy (sad songs in the catalog are calm)
SAD_BUT_HYPED = {
    "favorite_genre": "folk",
    "favorite_mood": "sad",
    "target_energy": 0.90,
    "likes_acoustic": False,
    "likes_instrumental": False,
}

# Conflict: wants angry metal but also acoustic, instrumental music
ACOUSTIC_HEADBANGER = {
    "favorite_genre": "metal",
    "favorite_mood": "angry",
    "target_energy": 0.95,
    "likes_acoustic": True,
    "likes_instrumental": True,
}

# Typo test: same as Pop / Happy but with capital letters
CAPITAL_LETTERS = {
    "favorite_genre": "Pop",
    "favorite_mood": "Happy",
    "target_energy": 0.80,
    "likes_acoustic": False,
    "likes_instrumental": False,
}

# Genre and mood that don't exist anywhere in the catalog
NOT_IN_CATALOG = {
    "favorite_genre": "k-pop",
    "favorite_mood": "dreamy",
    "target_energy": 0.70,
    "likes_acoustic": False,
    "likes_instrumental": False,
}

# Energy outside the 0-1 range
ENERGY_TOO_HIGH = {
    "favorite_genre": "edm",
    "favorite_mood": "euphoric",
    "target_energy": 1.50,
    "likes_acoustic": False,
    "likes_instrumental": False,
}

# --- Profiles that use the advanced features ---

# Rock fan who also likes metal-ish vibes, 2000s music, and live recordings
ROCK_WITH_TAGS = {
    "favorite_genre": "rock",
    "favorite_mood": "intense",
    "target_energy": 0.90,
    "likes_acoustic": False,
    "likes_instrumental": False,
    "wanted_tags": ["intense", "aggressive", "dark"],
    "target_popularity": 50,
    "favorite_decade": 2000,
    "likes_live": True,
    "likes_rap": False,
}

# Someone who wants older, warm, less-known songs
NOSTALGIC_HIDDEN_GEMS = {
    "favorite_genre": "country",
    "favorite_mood": "nostalgic",
    "target_energy": 0.50,
    "likes_acoustic": True,
    "likes_instrumental": False,
    "wanted_tags": ["nostalgic", "warm"],
    "target_popularity": 30,
    "favorite_decade": 1990,
    "likes_live": True,
    "likes_rap": False,
}

PROFILES = [
    ("Pop / Happy", POP_HAPPY),
    ("Study Session", STUDY_SESSION),
    ("Deep Intense Rock", DEEP_INTENSE_ROCK),
    ("Edge Case: Sad but Hyped", SAD_BUT_HYPED),
    ("Edge Case: Acoustic Headbanger", ACOUSTIC_HEADBANGER),
    ("Edge Case: Capital Letters", CAPITAL_LETTERS),
    ("Edge Case: Not in Catalog", NOT_IN_CATALOG),
    ("Edge Case: Energy Too High", ENERGY_TOO_HIGH),
    ("Advanced: Rock with Mood Tags", ROCK_WITH_TAGS),
    ("Advanced: Nostalgic Hidden Gems", NOSTALGIC_HIDDEN_GEMS),
]


def print_recommendations(name: str, user_prefs: dict, recommendations: list, top_score: float) -> None:
    """Prints a profile header followed by each recommended song, its score, and its reasons."""
    yes_no = lambda value: "yes" if value else "no"
    line = "=" * 60

    print(line)
    print(f"  Profile: {name}")
    print(
        f"  genre={user_prefs['favorite_genre']} | mood={user_prefs['favorite_mood']} | "
        f"energy={user_prefs['target_energy']:.2f} | "
        f"acoustic={yes_no(user_prefs['likes_acoustic'])} | "
        f"instrumental={yes_no(user_prefs['likes_instrumental'])}"
    )
    if "wanted_tags" in user_prefs:
        print(
            f"  tags={'/'.join(user_prefs['wanted_tags'])} | "
            f"popularity={user_prefs['target_popularity']} | "
            f"decade={user_prefs['favorite_decade']}s | "
            f"live={yes_no(user_prefs['likes_live'])} | "
            f"rap={yes_no(user_prefs['likes_rap'])}"
        )
    print(line)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n  #{rank}  {song['title']}  ({song['artist']})")
        print(f"      Score: {score:.2f} / {top_score:.2f}")
        print("      Why:")
        for reason in explanation.split(", "):
            print(f"        - {reason}")
    print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Music Recommender Simulation")
    parser.add_argument("--mode", choices=STRATEGIES.keys(), default="balanced",
                        help="which scoring mode to rank songs with")
    strategy = STRATEGIES[parser.parse_args().mode]

    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")
    print(f"Scoring mode: {strategy.name} ({strategy.description})\n")

    for name, user_prefs in PROFILES:
        recommendations = recommend_songs(user_prefs, songs, k=5, strategy=strategy)
        print_recommendations(name, user_prefs, recommendations, max_score(user_prefs, strategy))


if __name__ == "__main__":
    main()
