# Czech Tech Events Bot 🇨🇿

A Telegram bot that automatically monitors Czech tech communities, universities,
event platforms, and conference websites and notifies users about newly published
IT events.

The project focuses primarily on tech events in:

- Olomouc
- Brno
- Prague

## Usage

Coming soon

## Goal

Tech events in Czechia are spread across many different websites and communities.

This project aggregates them into one place and sends a Telegram notification
whenever a new relevant event appears.

The bot monitors event sources periodically, extracts event information,
filters IT-related events, detects duplicates, and sends only events that have
not been sent before.

## Example notification

🔥 **New IT event in Prague**

**DevFest Czechia 2026**

📅 30 October 2026, 09:00  
📍 Prague  
💰 Free  
🏷 Software Development, Cloud, AI

🔗 Event page

## Sources

Initial sources monitored by the bot:

### Olomouc

- VTP UP
- UPOL Department of Computer Science

### Czech Republic / Multi-city

- Meetup
- Luma
- dev.events
- UA IT Community Czech (`@uaitinczech`)
- GDG

### Brno

- Brno.AI
- JIC
- FIT VUT
- FI MUNI

### Prague

- prg.ai

More sources will be added later.

## Current status

The current local MVP supports the VTP UP events page. It can:

- fetch and parse VTP UP event listings;
- normalize listings into a common `Event` model;
- filter past and non-IT events;
- remove duplicate events;
- remember previously processed events in `data/seen_events.json`;
- print new events to the terminal.

Telegram notifications, automatic scheduling, and the remaining event sources
have not been implemented yet.

## Setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run

Run the application from the project root:

```bash
python -m app.main
```

## Tests

Run the complete test suite from the project root:

```bash
python -m pytest
```
