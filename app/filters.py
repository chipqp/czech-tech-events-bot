from datetime import date
import re
import unicodedata

from app.models import Event


IT_KEYWORDS: set[str] = {
    # General software and IT
    "software",
    "software development",
    "software engineering",
    "developer",
    "developers",
    "programming",
    "computer science",
    "information technology",
    "open source",
    "developer tools",
    "software architecture",
    "system design",

    # Czech software and IT
    "vývoj software",
    "vývoj softwaru",
    "softwarový vývoj",
    "vývojář",
    "vývojáři",
    "vývojáře",
    "programování",
    "informatika",
    "informační technologie",
    "otevřený software",
    "architektura software",

    # Artificial intelligence
    "ai",
    "artificial intelligence",
    "machine learning",
    "deep learning",
    "generative ai",
    "genai",
    "llm",
    "large language model",
    "large language models",
    "rag",
    "neural network",
    "neural networks",
    "computer vision",
    "natural language processing",
    "nlp",

    # Czech artificial intelligence
    "umělá inteligence",
    "strojové učení",
    "hluboké učení",
    "generativní ai",
    "jazykový model",
    "jazykové modely",
    "neuronová síť",
    "neuronové sítě",
    "počítačové vidění",
    "zpracování přirozeného jazyka",

    # Web development
    "backend",
    "back end",
    "frontend",
    "front end",
    "fullstack",
    "full stack",
    "web development",
    "web application",
    "microservices",
    "distributed systems",
    "event driven architecture",

    # Czech web development
    "webový vývoj",
    "webová aplikace",
    "mikroslužby",
    "distribuované systémy",

    # Programming languages
    "python",
    "javascript",
    "typescript",
    "java",
    "kotlin",
    "swift",
    "dart",
    "golang",
    "rust",
    "php",
    "ruby",
    "c++",
    "c#",
    ".net",

    # Frameworks and platforms
    "react",
    "angular",
    "vue",
    "node.js",
    "django",
    "flask",
    "spring",
    "laravel",

    # Mobile development
    "mobile development",
    "android development",
    "ios development",
    "android",
    "ios",
    "flutter",

    # Cloud and DevOps
    "cloud",
    "cloud computing",
    "devops",
    "docker",
    "kubernetes",
    "containers",
    "aws",
    "azure",
    "google cloud",
    "gcp",
    "linux",
    "ci/cd",
    "site reliability engineering",
    "sre",
    "infrastructure as code",
    "terraform",
    "ansible",

    # Data and databases
    "data science",
    "data engineering",
    "data analytics",
    "big data",
    "database",
    "databases",
    "sql",
    "postgresql",
    "mysql",
    "mongodb",
    "redis",
    "data visualization",

    # Czech data and databases
    "datová věda",
    "datové inženýrství",
    "datová analytika",
    "databáze",
    "vizualizace dat",

    # Cybersecurity
    "cybersecurity",
    "cyber security",
    "information security",
    "application security",
    "network security",
    "ethical hacking",
    "penetration testing",
    "infosec",
    "cryptography",

    # Czech cybersecurity
    "kyberbezpečnost",
    "kybernetická bezpečnost",
    "informační bezpečnost",
    "aplikační bezpečnost",
    "síťová bezpečnost",
    "etický hacking",
    "penetrační testování",
    "kryptografie",

    # Networks and infrastructure
    "computer networks",
    "network engineering",
    "network infrastructure",
    "počítačové sítě",
    "síťové technologie",

    # Testing and QA
    "software testing",
    "automated testing",
    "test automation",
    "quality assurance",
    "qa",
    "testování software",
    "automatizované testování",
    "zajištění kvality",

    # APIs and development tools
    "api",
    "apis",
    "rest api",
    "graphql",
    "git",
    "github",
    "gitlab",
    "version control",

    # Hardware and embedded systems
    "embedded",
    "embedded systems",
    "firmware",
    "iot",
    "internet of things",
    "robotics",
    "microcontroller",
    "arduino",
    "raspberry pi",
    "hardware",
    "vestavěné systémy",
    "internet věcí",
    "robotika",

    # Tech events and careers
    "hackathon",
    "hackaton",
    "coding",
    "code camp",
    "devfest",
    "developer meetup",
    "programming meetup",
    "developer conference",
    "tech conference",
    "it career",
    "tech career",
    "vývojářská konference",
    "programátorský meetup",
    "programátorská soutěž",
    "technologická konference",
}


def filter_upcoming_events(events: list[Event]) -> list[Event]:
    """Filter events that occur today or in the future."""
    upcoming_events: list[Event] = []
    today = date.today()

    for event in events:
        event_date = date.fromisoformat(event.date)

        if event_date >= today:
            upcoming_events.append(event)

    return upcoming_events


def normalize_text(text: str) -> str:
    """Normalize text for keyword matching and event fingerprints.

    Convert text to a case-insensitive form, preserve special technology names through
    replacements (for example, ``C++`` becomes ``cpp``), remove diacritics
    and punctuation, and collapse repeated whitespace into single spaces.
    """
    text = text.casefold()

    replacements = {
        "c++": "cpp",
        "c#": "csharp",
        ".net": "dotnet",
        "node.js": "nodejs",
        "ci/cd": "cicd",
        "full-stack": "full stack",
    }

    for original, replacement in replacements.items():
        if original in text:
            text = text.replace(original, replacement)

    text = unicodedata.normalize("NFKD", text)
    text = "".join(
        character for character in text if not unicodedata.combining(character)
    )
    text = re.sub(r"[^a-z0-9]+", " ", text)
    text = " ".join(text.split())

    return text


def contains_keyword(text: str, keyword: str) -> bool:
    """Return whether the text contains the complete keyword."""
    text = normalize_text(text)
    keyword = normalize_text(keyword)

    text = " " + text + " "
    keyword = " " + keyword + " "

    return keyword in text


def filter_it_events(events: list[Event]) -> list[Event]:
    """Filter events by checking if they are IT related."""
    relevant_events: list[Event] = []

    for event in events:
        categories_text = " ".join(event.categories)

        for keyword in IT_KEYWORDS:
            if (
                contains_keyword(event.title, keyword)
                or contains_keyword(categories_text, keyword)
            ):
                relevant_events.append(event)
                break

    return relevant_events


def filter_events(events: list[Event]) -> list[Event]:
    """Filter events by removing past date events and not IT relevant events."""
    filtered_events = filter_it_events(filter_upcoming_events(events))
    return filtered_events
