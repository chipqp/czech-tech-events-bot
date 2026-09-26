# Czech Tech Events Bot — Agent Instructions

## Project overview

This repository contains a Python project called **Czech Tech Events Bot**.

The goal is to build a small automated service that monitors selected Czech IT event websites and communities, detects newly published events, removes duplicates, and sends new events to the user through Telegram.

The project is currently in the early MVP stage.

Do not overengineer the first version.

---

## V1 goal

Version 1 should:

1. Periodically retrieve events from configured sources.
2. Parse event information.
3. Convert all events into one common `Event` model.
4. Filter events using IT-related keywords.
5. Detect duplicates across different sources.
6. Detect whether an event has already been sent before.
7. Send only new events to Telegram.
8. Store previously processed events locally.

Scheduling frequency will be decided later.

GitHub Actions will eventually run the monitor automatically, but this does not need to be implemented immediately.

---

## Event sources for V1

Initial sources:

### Olomouc
- VTP UP
- UPOL Katedra informatiky

### General / multi-city
- Meetup
- Luma
- dev.events
- Telegram channel `@uaitinczech`
- GDG

### Brno
- Brno.AI
- JIC
- FIT VUT
- FI MUNI

### Prague
- prg.ai

Do not add additional sources unless requested.

Each source should have its own parser module under:

`app/sources/`

---

## Current project structure

```text
czech-tech-events-bot/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── models.py
│   ├── filters.py
│   ├── dedup.py
│   ├── telegram_bot.py
│   │
│   └── sources/
│       ├── __init__.py
│       ├── vtp_up.py
│       ├── upol_informatics.py
│       ├── meetup.py
│       ├── luma.py
│       ├── dev_events.py
│       ├── telegram_uait.py
│       ├── brno_ai.py
│       ├── jic.py
│       ├── fit_vut.py
│       ├── fi_muni.py
│       ├── prg_ai.py
│       └── gdg.py
│
├── data/
│   └── seen_events.json
│
├── tests/
│   └── __init__.py
│
├── .github/
│   └── workflows/
│       └── monitor.yml
│
├── .env.example
├── .gitignore
├── requirements.txt
├── AGENTS.md
└── README.md

## Python environment

The project uses a local virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Currently installed dependencies include:

- requests
- beautifulsoup4
- python-dotenv

Dependencies are stored in:

`requirements.txt`

Prefer adding dependencies only when they are actually necessary.

---

## Event model

All source parsers must return the same normalized event structure.

The intended model is approximately:

```python
from dataclasses import dataclass

@dataclass
class Event:
    title: str
    date: str
    city: str
    venue: str | None
    price: str | None
    categories: list[str]
    url: str
    source: str
```

This model may evolve if necessary, for example by using `datetime`, but keep it simple during V1.

---

## Event notification format

Telegram messages should eventually look approximately like this:

```text
🔥 New IT event in Prague

DevFest Czechia 2026

📅 30 October 2026, 09:00
📍 Prague Congress Centre
💰 Free
🏷 Software Development, Cloud, AI

🔗 https://event-page.example
```

Required information when available:

- title
- date
- time
- city
- venue
- price
- categories
- event URL

If some information cannot be found, do not invent it.

For example:

```text
price = "Unknown"
```

is preferable to assuming an event is free.

---

## Filtering

V1 uses keyword-based filtering.

The bot should monitor IT broadly, not only AI.

Relevant categories include:

- Software Development
- Backend
- Frontend
- Full-stack
- Python
- Java
- JavaScript
- TypeScript
- C
- C++
- C#
- .NET
- Mobile Development
- Cloud
- DevOps
- Linux
- Open Source
- Cybersecurity
- Data
- Databases
- AI
- Machine Learning
- Embedded Systems
- Networking
- Web Development
- Software Architecture
- Developer Tools
- Testing / QA
- APIs
- Containers
- Kubernetes
- Hackathons
- Developer conferences
- IT career events
- Student IT events

AI-based classification is NOT part of V1.

A future version may allow users to select preferred categories.

---

## Deduplication

The same event can appear on multiple sources.

Example:

```text
Meetup
GDG
dev.events
Brno.AI
```

may all list the same conference.

Do not deduplicate only by URL.

Use a normalized event fingerprint based primarily on:

```text
normalized title + date + city
```

A hash of that value may be used internally.

Normalization should handle obvious differences such as:

- capitalization
- extra whitespace
- punctuation

Do not make fuzzy matching unnecessarily complex in V1.

---

## Seen events

Previously processed events are initially stored in:

`data/seen_events.json`

The bot should not send the same event repeatedly on every execution.

SQLite may replace JSON later, but do not introduce a database during the first implementation unless requested.

---

## Source parser design

Each source module should expose a simple function such as:

```python
def get_events() -> list[Event]:
    ...
```

or a similarly simple interface.

Source-specific parsing logic must stay inside the respective source module.

Avoid putting website-specific selectors or parsing code into `main.py`.

Prefer:

```text
source website
    ↓
source parser
    ↓
Event objects
```

rather than exposing raw HTML to the rest of the application.

---

## Scraping rules

Prefer the simplest reliable data source in this order:

1. RSS / Atom
2. iCal / structured feeds
3. documented public APIs
4. server-rendered HTML
5. JavaScript/browser automation only if necessary

Do not introduce Playwright or Selenium until a source genuinely requires JavaScript rendering.

Use reasonable request timeouts.

Send an identifiable User-Agent where appropriate.

A failure in one source should not crash the entire monitoring run.

Log the source that failed and continue with the remaining sources.

---

## Telegram source

`@uaitinczech` is one of the V1 sources.

For the first implementation, prefer parsing the public Telegram preview page if possible:

```text
https://t.me/s/uaitinczech
```

Do not introduce Telegram user authentication or Telethon unless the public preview proves insufficient.

Telegram Bot API will later be used for sending notifications.

---

## Telegram secrets

Telegram credentials must never be committed.

Local secrets will eventually be stored in:

`.env`

Example:

```env
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
```

`.env.example` may be committed.

`.env` must remain ignored by Git.

---

## Development strategy

Build the project incrementally.

Preferred order:

1. Implement `Event` model.
2. Implement one simple source parser.
3. Print parsed events to the terminal.
4. Add tests for parsing.
5. Add more sources one by one.
6. Implement keyword filtering.
7. Implement cross-source deduplication.
8. Implement `seen_events.json`.
9. Implement Telegram sending.
10. Add GitHub Actions scheduling.

Do not try to implement all twelve parsers at once.

The first source to implement should be **VTP UP**, unless the user requests another source.

---

## Code quality

Use:

- Python type hints
- small functions
- readable names
- clear module boundaries
- standard library where practical

Avoid:

- unnecessary abstractions
- premature OOP hierarchies
- giant classes
- unnecessary frameworks
- hidden magic
- adding a database too early

For parsing, prefer small helper functions that can be tested separately.

---

## Testing

Parser code should ideally be testable without repeatedly making real network requests.

When useful, store small HTML fixtures under:

```text
tests/fixtures/
```

At minimum, test:

- event title extraction
- date extraction
- URL extraction
- duplicate fingerprint generation
- keyword filtering

Run relevant tests after making changes.

---

## Working style for Codex

Before implementing a task:

1. Read this `AGENTS.md`.
2. Read `README.md`.
3. Inspect the existing code before modifying it.
4. Preserve existing working behavior.
5. Make focused changes rather than rewriting unrelated parts.

When completing a task:

- briefly explain what changed
- mention files changed
- mention commands/tests run
- mention any assumptions or unresolved issues

If the structure of an external website is uncertain, inspect it before writing selectors.

Do not fabricate selectors, API endpoints, event data, or undocumented behavior.

If a scraper cannot reliably extract a required field, represent the value as unknown rather than guessing.

---

## Current immediate milestone

The project has just been initialized.

The Python virtual environment has been created and the initial dependencies installed.

The next implementation milestone is:

1. Create the normalized `Event` model in `app/models.py`.
2. Investigate the current VTP UP events page.
3. Implement the first VTP UP parser in `app/sources/vtp_up.py`.
4. Make it possible to run the parser locally and print normalized events.
5. Add a small test if practical.

Do NOT implement Telegram sending, GitHub Actions, or all other sources yet.