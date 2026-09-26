from app.models import Event
from app.sources.vtp_up import EVENTS_URL, parse_events


SAMPLE_HTML = """
<html>
  <body>
    <h3>Blížící se akce aneb co pro vás v roce 2026 plánujeme</h3>
    <h4>
      <ul>
        <li></li>
        <li><b>4. 2. 2026&nbsp;&nbsp;Business Spot</b></li>
        <li><b>12. 11. 2026&nbsp;&nbsp;UP Business Camp</b></li>
      </ul>
    </h4>
  </body>
</html>
"""


def test_parses_events() -> None:
    events = parse_events(SAMPLE_HTML)

    assert len(events) == 2

    first_event = events[0]
    assert isinstance(first_event, Event)
    assert first_event.title == "Business Spot"
    assert first_event.date == "2026-02-04"
    assert first_event.city == "Olomouc"
    assert first_event.url == EVENTS_URL
    assert first_event.source == "VTP UP"

    second_event = events[1]
    assert second_event.title == "UP Business Camp"
    assert second_event.date == "2026-11-12"
