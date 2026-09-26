from pathlib import Path

from app.storage import load_seen_fingerprints, save_seen_fingerprints


def test_load_seen_fingerprints(tmp_path: Path) -> None:
    seen_events_path = tmp_path / "seen_events.json"
    seen_events_path.write_text(
        '["python workshop|2030-12-09|olomouc", '
        '"devfest|2030-10-30|prague"]',
        encoding="utf-8",
    )

    fingerprints = load_seen_fingerprints(seen_events_path)

    assert fingerprints == {
        "python workshop|2030-12-09|olomouc",
        "devfest|2030-10-30|prague",
    }


def test_load_seen_fingerprints_when_file_does_not_exist(tmp_path: Path) -> None:
    missing_path = tmp_path / "missing.json"

    fingerprints = load_seen_fingerprints(missing_path)

    assert fingerprints == set()


def test_save_and_load_seen_fingerprints(tmp_path: Path) -> None:
    seen_events_path = tmp_path / "seen_events.json"
    fingerprints = {
        "python workshop|2030-12-09|olomouc",
        "devfest|2030-10-30|prague",
    }

    save_seen_fingerprints(fingerprints, seen_events_path)
    loaded_fingerprints = load_seen_fingerprints(seen_events_path)

    assert loaded_fingerprints == fingerprints
