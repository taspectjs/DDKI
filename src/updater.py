import requests
from packaging.version import Version

GITHUB_API = "https://api.github.com/repos/YOUR_USER/DDKI/releases/latest"


def check_for_update(current_version: str) -> dict | None:
    """Returns release info dict if a newer version exists, else None."""
    try:
        resp = requests.get(GITHUB_API, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        latest = data.get("tag_name", "").lstrip("v")
        if Version(latest) > Version(current_version):
            return {
                "version": latest,
                "url": data.get("html_url", ""),
                "notes": data.get("body", ""),
            }
    except Exception:
        pass
    return None
