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
