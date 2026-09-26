from datetime import datetime

import requests
from bs4 import BeautifulSoup

from app.models import Event


EVENTS_URL = "https://www.vtpup.cz/akce"
USER_AGENT = "CzechTechEventsBot/0.1"


def fetch_page() -> str:
    response = requests.get(
        EVENTS_URL,
        headers={"User-Agent": USER_AGENT},
        timeout=10,
    )
    response.raise_for_status()
    return response.text


def parse_events(html: str) -> list[Event]:
    soup = BeautifulSoup(html, "html.parser")
    headings = soup.find_all("h3")

    events_heading = None

    for heading in headings:
        if "Blížící se akce" in heading.get_text():
            events_heading = heading
            break

    if events_heading is None:
        raise ValueError("Section with events wasn't found")

    events_block = events_heading.find_next_sibling("h4")

    if events_block is None:
        raise ValueError("List of events wasn't found")

    items = events_block.find_all("li")
    events: list[Event] = []

    for item in items:
        text = item.get_text(" ", strip=True)

        if not text:
            continue

        parts = text.split(maxsplit=3)

        if len(parts) != 4:
            continue

        date_text = " ".join(parts[:3])
        title = parts[3]

        event_date = datetime.strptime(date_text, "%d. %m. %Y").date().isoformat()

        events.append(
            Event(
                title=title,
                date=event_date,
                city="Olomouc",
                venue=None,
                price=None,
                categories=[],
                url=EVENTS_URL,
                source="VTP UP",
            )
        )

    return events


def get_events() -> list[Event]:
    html = fetch_page()
    return parse_events(html)
