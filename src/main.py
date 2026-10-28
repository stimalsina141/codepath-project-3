"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs

MAX_SCORE = 5.0

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

PROFILES = [
    ("Pop / Happy", POP_HAPPY),
    ("Study Session", STUDY_SESSION),
    ("Deep Intense Rock", DEEP_INTENSE_ROCK),
    ("Edge Case: Sad but Hyped", SAD_BUT_HYPED),
    ("Edge Case: Acoustic Headbanger", ACOUSTIC_HEADBANGER),
    ("Edge Case: Capital Letters", CAPITAL_LETTERS),
    ("Edge Case: Not in Catalog", NOT_IN_CATALOG),
    ("Edge Case: Energy Too High", ENERGY_TOO_HIGH),
]


def print_recommendations(name: str, user_prefs: dict, recommendations: list) -> None:
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
    print(line)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n  #{rank}  {song['title']}  ({song['artist']})")
        print(f"      Score: {score:.2f} / {MAX_SCORE:.2f}")
        print("      Why:")
        for reason in explanation.split(", "):
            print(f"        - {reason}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")

    for name, user_prefs in PROFILES:
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print_recommendations(name, user_prefs, recommendations)


if __name__ == "__main__":
    main()
