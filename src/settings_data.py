import json
from pathlib import Path

SETTINGS_FILE = Path.home() / ".ddki_settings.json"


def load_routes() -> list[str]:
    if not SETTINGS_FILE.exists():
        return []
    try:
        return json.loads(SETTINGS_FILE.read_text()).get("routes", [])
    except Exception:
        return []


def save_routes(routes: list[str]):
    data = {}
    if SETTINGS_FILE.exists():
        try:
            data = json.loads(SETTINGS_FILE.read_text())
        except Exception:
            pass
    data["routes"] = routes
    SETTINGS_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False))


def load_theme() -> str:
    if not SETTINGS_FILE.exists():
        return "light"
    try:
        return json.loads(SETTINGS_FILE.read_text()).get("theme", "light")
    except Exception:
        return "light"


def save_theme(name: str):
    data = {}
    if SETTINGS_FILE.exists():
        try:
            data = json.loads(SETTINGS_FILE.read_text())
        except Exception:
            pass
    data["theme"] = name
    SETTINGS_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False))
