import json
from pathlib import Path


SEEN_EVENTS_PATH = Path(__file__).parent.parent / "data" / "seen_events.json"


def load_seen_fingerprints(path: Path = SEEN_EVENTS_PATH) -> set[str]:
    """Load json file with fingerprints and return them as a set"""
    try:
        with open(path, "r", encoding="utf-8") as file:
            fingerprints = set(json.load(file))
            return fingerprints
    except FileNotFoundError:
        return set()


def save_seen_fingerprints(fingerprints: set[str], path: Path = SEEN_EVENTS_PATH) -> None:
    """Save seen event fingerprints to a JSON file."""
    fingerprints_to_save = sorted(fingerprints)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(fingerprints_to_save, file, indent=2)
  