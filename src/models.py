import json
from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import date

DATA_FILE = Path.home() / ".ddki_data.json"


@dataclass
class Entry:
    date: str      # DD.MM.YY
    location: str
    km: str        # can be empty


def current_month_key() -> str:
    today = date.today()
    return f"{today.month:02d}.{today.year}"


def load_data() -> dict[str, list[Entry]]:
    if not DATA_FILE.exists():
        return {}
    try:
        raw = json.loads(DATA_FILE.read_text())
        return {month: [Entry(**e) for e in entries] for month, entries in raw.items()}
    except Exception:
        return {}


def save_data(data: dict[str, list[Entry]]):
    raw = {month: [asdict(e) for e in entries] for month, entries in data.items()}
    DATA_FILE.write_text(json.dumps(raw, indent=2, ensure_ascii=False))


def month_label(key: str) -> str:
    MONTHS = ["Jan", "Feb", "Mär", "Apr", "Mai", "Jun",
              "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"]
    try:
        m, y = key.split(".")
        return f"{MONTHS[int(m) - 1]} {y}"
    except Exception:
        return key
