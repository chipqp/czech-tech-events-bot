from requests.exceptions import RequestException

from app.sources.vtp_up import get_events
from app.filters import filter_events
from app.storage import load_seen_fingerprints, save_seen_fingerprints
from app.dedup import (
    event_fingerprint, 
    get_unseen_events,
    remove_duplicate_events, 
)


def main() -> None:
    try:
        events = get_events()
    except RequestException as error:
        print(f"Failed to fetch VTP UP events: {error}")
        return
    except ValueError as error:
        print(f"Failed to parse VTP UP events: {error}")
        return

    events = filter_events(events)
    events = remove_duplicate_events(events)

    seen_fingerprints = load_seen_fingerprints()
    unseen_events = get_unseen_events(events, seen_fingerprints)

    if not unseen_events:
        print("No new events found.")
        return

    for event in unseen_events:
        print(f"\n{event.title}")
        print(f"Date: {event.date}")
        print(f"City: {event.city}")
        print(f"Venue: {event.venue}")
        print(f"Price: {event.price}")
        print(f"Categories: {event.categories}")
        print(f"Url: {event.url}")
        print(f"Source: {event.source}")

        seen_fingerprints.add(event_fingerprint(event))

    save_seen_fingerprints(seen_fingerprints)


if __name__ == "__main__":
    main()
