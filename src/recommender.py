import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict, field


@dataclass(frozen=True)
class ScoringStrategy:
    """A scoring mode: one set of weights that score_song uses to judge songs."""
    name: str
    description: str
    genre: float = 2.0
    mood: float = 1.0
    energy: float = 1.0
    acoustic: float = 0.5
    instrumental: float = 0.5
    # Advanced features (only scored when the user sets them)
    mood_tag: float = 0.5     # per shared tag, up to MAX_TAGS_COUNTED tags
    popularity: float = 0.5
    decade: float = 0.5
    live: float = 0.5
    rap: float = 0.5


MAX_TAGS_COUNTED = 2

# Balanced = the original recipe (max 5.0 on the basic features).
# Experiment tried: genre 1.0 / energy 2.0 -> mostly same rankings, so kept the original
BALANCED = ScoringStrategy("Balanced", "Genre counts most, then mood and energy")
GENRE_FIRST = ScoringStrategy("Genre-First", "Sticks to your favorite genre above everything else",
                              genre=3.0, mood=0.5, energy=0.5)
MOOD_FIRST = ScoringStrategy("Mood-First", "Cares most about the feeling, even across genres",
                             genre=0.5, mood=2.5, mood_tag=1.0)
ENERGY_FOCUSED = ScoringStrategy("Energy-Focused", "Cares most about how calm or intense a song is",
                                 genre=1.0, mood=0.5, energy=3.0)

STRATEGIES = {
    "balanced": BALANCED,
    "genre-first": GENRE_FIRST,
    "mood-first": MOOD_FIRST,
    "energy-focused": ENERGY_FOCUSED,
}


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
    popularity: int = 0
    release_decade: int = 0
    mood_tags: List[str] = field(default_factory=list)
    liveness: float = 0.0
    speechiness: float = 0.0

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
    # Optional advanced preferences (None = don't care)
    wanted_tags: Optional[List[str]] = None
    target_popularity: Optional[int] = None
    favorite_decade: Optional[int] = None
    likes_live: Optional[bool] = None
    likes_rap: Optional[bool] = None

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song], strategy: ScoringStrategy = BALANCED):
        self.songs = songs
        self.strategy = strategy

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns the top k songs for this user, highest score first (uses score_song)."""
        user_prefs = asdict(user)
        ranked = sorted(
            self.songs,
            key=lambda song: score_song(user_prefs, asdict(song), self.strategy)[0],
            reverse=True,
        )
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns the song's score and the reasons it earned its points, as one sentence."""
        score, reasons = score_song(asdict(user), asdict(song), self.strategy)
        return f"Score {score:.2f}: " + ", ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """Reads songs.csv into a list of dicts, turning the number columns into ints and floats."""
    int_fields = ["id", "popularity", "release_decade"]
    float_fields = ["energy", "tempo_bpm", "valence", "danceability", "acousticness",
                    "instrumentalness", "liveness", "speechiness"]

    songs = []
    with open(csv_path, newline="") as f:
        for row in csv.DictReader(f):
            for name in int_fields:
                row[name] = int(row[name])
            for name in float_fields:
                row[name] = float(row[name])
            row["mood_tags"] = row["mood_tags"].split(";")
            songs.append(row)
    return songs

def is_set(user_prefs: Dict, key: str) -> bool:
    """True if the user filled in this optional preference."""
    return user_prefs.get(key) is not None

def max_score(user_prefs: Dict, strategy: ScoringStrategy = BALANCED) -> float:
    """The highest score any song could get for this user under this strategy."""
    total = strategy.genre + strategy.mood + strategy.energy + strategy.acoustic + strategy.instrumental
    if is_set(user_prefs, "wanted_tags"):
        total += strategy.mood_tag * min(MAX_TAGS_COUNTED, len(user_prefs["wanted_tags"]))
    if is_set(user_prefs, "target_popularity"):
        total += strategy.popularity
    if is_set(user_prefs, "favorite_decade"):
        total += strategy.decade
    if is_set(user_prefs, "likes_live"):
        total += strategy.live
    if is_set(user_prefs, "likes_rap"):
        total += strategy.rap
    return total

def score_song(user_prefs: Dict, song: Dict, strategy: ScoringStrategy = BALANCED) -> Tuple[float, List[str]]:
    """Scores one song against the user's taste and returns (score, list of reasons)."""
    w = strategy
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs["favorite_genre"]:
        score += w.genre
        reasons.append(f"genre match (+{w.genre:.1f})")

    if song["mood"] == user_prefs["favorite_mood"]:
        score += w.mood
        reasons.append(f"mood match (+{w.mood:.1f})")

    # Closer to the target energy = more points (max w.energy)
    energy_points = w.energy * (1 - abs(song["energy"] - user_prefs["target_energy"]))
    score += energy_points
    reasons.append(f"energy close to target (+{energy_points:.2f})")

    # A song counts as acoustic / instrumental if its value is 0.5 or higher
    song_is_acoustic = song["acousticness"] >= 0.5
    if song_is_acoustic == user_prefs["likes_acoustic"]:
        score += w.acoustic
        reasons.append(f"acoustic preference match (+{w.acoustic:.1f})")

    song_is_instrumental = song["instrumentalness"] >= 0.5
    if song_is_instrumental == user_prefs["likes_instrumental"]:
        score += w.instrumental
        reasons.append(f"instrumental preference match (+{w.instrumental:.1f})")

    # --- Advanced features: only scored when the user set that preference ---

    if is_set(user_prefs, "wanted_tags"):
        shared = [tag for tag in user_prefs["wanted_tags"] if tag in song["mood_tags"]]
        if shared:
            tag_points = w.mood_tag * min(MAX_TAGS_COUNTED, len(shared))
            score += tag_points
            reasons.append(f"mood tags {'/'.join(shared)} (+{tag_points:.1f})")

    # Popularity is 0-100, so the gap is divided by 100 to keep it between 0 and 1
    if is_set(user_prefs, "target_popularity"):
        pop_points = w.popularity * (1 - abs(song["popularity"] - user_prefs["target_popularity"]) / 100)
        score += pop_points
        reasons.append(f"popularity close to target (+{pop_points:.2f})")

    # Exact decade = full points, one decade off = half points
    if is_set(user_prefs, "favorite_decade"):
        decade_gap = abs(song["release_decade"] - user_prefs["favorite_decade"])
        if decade_gap == 0:
            score += w.decade
            reasons.append(f"from the {song['release_decade']}s (+{w.decade:.1f})")
        elif decade_gap == 10:
            score += w.decade / 2
            reasons.append(f"close decade: {song['release_decade']}s (+{w.decade / 2:.2f})")

    # Liveness 0.5+ sounds like a live recording
    if is_set(user_prefs, "likes_live"):
        if (song["liveness"] >= 0.5) == user_prefs["likes_live"]:
            score += w.live
            reasons.append(f"live recording preference match (+{w.live:.1f})")

    # Speechiness 0.33+ means a lot of rapping or talking
    if is_set(user_prefs, "likes_rap"):
        if (song["speechiness"] >= 0.33) == user_prefs["likes_rap"]:
            score += w.rap
            reasons.append(f"rap/spoken vocals preference match (+{w.rap:.1f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5,
                    strategy: ScoringStrategy = BALANCED) -> List[Tuple[Dict, float, str]]:
    """Scores every song, sorts them highest first, and returns the top k as (song, score, explanation)."""
    # Judge every song with score_song
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, strategy)
        scored.append((song, score, ", ".join(reasons)))

    # Highest score first, then keep the top k
    ranked = sorted(scored, key=lambda item: item[1], reverse=True)
    return ranked[:k]
