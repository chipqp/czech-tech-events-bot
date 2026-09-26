from app.dedup import (
    event_fingerprint,
    get_unseen_events,
    remove_duplicate_events,
)
from app.models import Event


def test_event_fingerprint() -> None:
    ai_event = Event(
        title="Ai workshop",
        date="2030-12-09",
        city="Olomouc",
        venue="Smeralova",
        price=None,
        categories=[],
        url="https://www.vtpup.cz/akce",
        source="source"
    )

    ai_event_fingerprint = "ai workshop|2030-12-09|olomouc"

    assert event_fingerprint(ai_event) == ai_event_fingerprint


def test_equivalent_events_have_same_fingerprint() -> None:
    first_event = Event(
        title="Python  Workshop!",
        date="2030-12-09",
        city="OLOMOUC",
        venue=None,
        price=None,
        categories=[],
        url="https://example.com/first",
        source="First source"
    )

    second_event = Event(
        title="python workshop",
        date="2030-12-09",
        city="Olomouc",
        venue="Smeralova",
        price="Free",
        categories=["Python"],
        url="https://example.com/second",
        source="Second source"
    )

    assert event_fingerprint(first_event) == event_fingerprint(second_event)


def test_remove_duplicate_events_keeps_first_event() -> None:
    first_event = Event(
        title="Python Workshop",
        date="2030-12-09",
        city="Olomouc",
        venue="First venue",
        price=None,
        categories=["Python"],
        url="https://example.com/first",
        source="First source"
    )

    duplicate_event = Event(
        title="python  workshop!",
        date="2030-12-09",
        city="OLOMOUC",
        venue="Second venue",
        price="Free",
        categories=[],
        url="https://example.com/duplicate",
        source="Second source"
    )

    event_on_different_date = Event(
        title="Python Workshop",
        date="2030-12-10",
        city="Olomouc",
        venue=None,
        price=None,
        categories=["Python"],
        url="https://example.com/different-date",
        source="First source"
    )

    events = [first_event, duplicate_event, event_on_different_date]

    unique_events = remove_duplicate_events(events)

    assert unique_events == [first_event, event_on_different_date]


def test_remove_duplicate_events_from_empty_list() -> None:
    assert remove_duplicate_events([]) == []


def test_get_unseen_events_returns_only_new_events() -> None:
    seen_event = Event(
        title="Python Workshop",
        date="2030-12-09",
        city="Olomouc",
        venue=None,
        price=None,
        categories=["Python"],
        url="https://example.com/seen",
        source="First source"
    )

    new_event = Event(
        title="DevFest",
        date="2030-12-10",
        city="Prague",
        venue=None,
        price=None,
        categories=["Software development"],
        url="https://example.com/new",
        source="Second source"
    )

    seen_fingerprints = {event_fingerprint(seen_event)}

    unseen_events = get_unseen_events(
        [seen_event, new_event],
        seen_fingerprints,
    )

    assert unseen_events == [new_event]


def test_get_unseen_events_with_empty_seen_set_returns_all_events() -> None:
    first_event = Event(
        title="Python Workshop",
        date="2030-12-09",
        city="Olomouc",
        venue=None,
        price=None,
        categories=["Python"],
        url="https://example.com/first",
        source="First source"
    )

    second_event = Event(
        title="DevFest",
        date="2030-12-10",
        city="Prague",
        venue=None,
        price=None,
        categories=["Software development"],
        url="https://example.com/second",
        source="Second source"
    )

    events = [first_event, second_event]

    assert get_unseen_events(events, set()) == events
