from app.models import Event
from app.filters import (
    contains_keyword,
    filter_events,
    filter_it_events,
    filter_upcoming_events,
    normalize_text,
)


def test_filter_upcoming_events() -> None:
    past_date = "2006-05-09"
    past_event = Event(
        title="Past event",
        date=past_date,
        city="city",
        venue=None,
        price=None,
        categories=["AI", "ML", "DL"],
        url="https://example.com/",
        source="source"
    )

    future_date = "2106-05-09"
    future_event = Event(
        title="Future event",
        date=future_date,
        city="city",
        venue=None,
        price=None,
        categories=["AI", "ML", "DL"],
        url="https://example.com/",
        source="source"
    )

    events_list = [past_event, future_event]

    filtered_events = filter_upcoming_events(events_list)

    assert filtered_events == [future_event]


def test_normalize_text() -> None:
    assert "umela inteligence" == normalize_text("  Umělá   inteligence  ")
    assert "python" == normalize_text("PYTHON")
    assert "cpp dotnet" == normalize_text("C++ / .NET")
    assert "nodejs" == normalize_text("Node.js")


def test_contains_keyword() -> None:
    assert contains_keyword("AI conference", "ai")
    assert not contains_keyword("Email marketing", "ai")
    assert contains_keyword("Machine Learning workshop", "machine learning")
    assert contains_keyword("C# workshop", "csharp")


def test_filter_it_events() -> None:
    # Relevant event by title
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

    # Relevant event by categories
    cybersecurity_event = Event(
        title="Event title",
        date="2030-12-09",
        city="Olomouc",
        venue="Smeralova",
        price=None,
        categories=["Cybersecurity", "network security"],
        url="https://www.vtpup.cz/akce",
        source="source"
    )

    # Irrelevant event
    irrelevant_event = Event(
        title="Event title",
        date="2030-12-09",
        city="Olomouc",
        venue="Smeralova",
        price=None,
        categories=["design", "art"],
        url="https://www.example.com",
        source="source"
    )

    events = [ai_event, cybersecurity_event, irrelevant_event]
    relevant_events = filter_it_events(events)
    assert relevant_events == [ai_event, cybersecurity_event]


def test_filter_events() -> None:
    future_it_event = Event(
        title="Python workshop",
        date="2106-05-09",
        city="Olomouc",
        venue=None,
        price=None,
        categories=[],
        url="https://example.com/future-it-event",
        source="source"
    )

    past_it_event = Event(
        title="Python workshop",
        date="2006-05-09",
        city="Olomouc",
        venue=None,
        price=None,
        categories=[],
        url="https://example.com/past-it-event",
        source="source"
    )

    future_irrelevant_event = Event(
        title="Art exhibition",
        date="2106-05-09",
        city="Olomouc",
        venue=None,
        price=None,
        categories=["art"],
        url="https://example.com/future-art-event",
        source="source"
    )

    events = [future_it_event, past_it_event, future_irrelevant_event]

    filtered_events = filter_events(events)

    assert filtered_events == [future_it_event]
