import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict

# Scoring weights (max score 5.0: 2.0 + 1.0 + 1.0 + 0.5 + 0.5)
# Experiment tried: genre 1.0 / energy 2.0 -> mostly same rankings, so kept the original
GENRE_WEIGHT = 2.0
MOOD_WEIGHT = 1.0
ENERGY_WEIGHT = 1.0

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float
    instrumentalness: float = 0.0

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    likes_instrumental: bool = False

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns the top k songs for this user, highest score first (uses score_song)."""
        user_prefs = asdict(user)
        ranked = sorted(self.songs, key=lambda song: score_song(user_prefs, asdict(song))[0], reverse=True)
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns the song's score and the reasons it earned its points, as one sentence."""
        score, reasons = score_song(asdict(user), asdict(song))
        return f"Score {score:.2f}: " + ", ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """Reads songs.csv into a list of dicts, turning the number columns into ints and floats."""
    float_fields = ["energy", "tempo_bpm", "valence", "danceability", "acousticness", "instrumentalness"]

    songs = []
    with open(csv_path, newline="") as f:
        for row in csv.DictReader(f):
            row["id"] = int(row["id"])
            for field in float_fields:
                row[field] = float(row[field])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores one song against the user's taste and returns (score, list of reasons)."""
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs["favorite_genre"]:
        score += GENRE_WEIGHT
        reasons.append(f"genre match (+{GENRE_WEIGHT:.1f})")

    if song["mood"] == user_prefs["favorite_mood"]:
        score += MOOD_WEIGHT
        reasons.append(f"mood match (+{MOOD_WEIGHT:.1f})")

    # Closer to the target energy = more points (max ENERGY_WEIGHT)
    energy_points = ENERGY_WEIGHT * (1 - abs(song["energy"] - user_prefs["target_energy"]))
    score += energy_points
    reasons.append(f"energy close to target (+{energy_points:.2f})")

    # A song counts as acoustic / instrumental if its value is 0.5 or higher
    song_is_acoustic = song["acousticness"] >= 0.5
    if song_is_acoustic == user_prefs["likes_acoustic"]:
        score += 0.5
        reasons.append("acoustic preference match (+0.5)")

    song_is_instrumental = song["instrumentalness"] >= 0.5
    if song_is_instrumental == user_prefs["likes_instrumental"]:
        score += 0.5
        reasons.append("instrumental preference match (+0.5)")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Scores every song, sorts them highest first, and returns the top k as (song, score, explanation)."""
    # Judge every song with score_song
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, ", ".join(reasons)))

    # Highest score first, then keep the top k
    ranked = sorted(scored, key=lambda item: item[1], reverse=True)
    return ranked[:k]
