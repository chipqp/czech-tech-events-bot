from app.filters import normalize_text
from app.models import Event


def event_fingerprint(event: Event) -> str:
    """Return a normalized fingerprint based on title, date, and city."""
    title = normalize_text(event.title)
    date = event.date
    city = normalize_text(event.city)

    fingerprint = title + "|" + date + "|" + city
    return fingerprint


def remove_duplicate_events(events: list[Event]) -> list[Event]:
    """Remove duplicate events while preserving their original order."""
    unique_fingerprints: set[str] = set()
    unique_events: list[Event] = []
    for event in events:
        fingerprint = event_fingerprint(event)

        if fingerprint not in unique_fingerprints:
            unique_fingerprints.add(fingerprint)
            unique_events.append(event)

    return unique_events


def get_unseen_events(events: list[Event], seen_fingerprints: set[str]) -> list[Event]:
    """Return events whose fingerprints are not in the seen set."""
    unseen_events = []

    for event in events:
        if event_fingerprint(event) not in seen_fingerprints:
            unseen_events.append(event)

    return unseen_events
