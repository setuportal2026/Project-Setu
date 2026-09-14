# modules/scrapper.py

import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime, timedelta

NOTIF_CACHE_PATH = os.path.join(os.path.dirname(__file__), "notifications_cache.json")
MMHAPU_HOME_URL = "https://mmhapu.ac.in/"
MAX_NOTICES = 10


def scrape_notifications() -> list[dict]:
    """Scrapes latest notification titles + PDF links from MMHAPU homepage."""
    try:
        response = requests.get(MMHAPU_HOME_URL, timeout=20)
        response.raise_for_status()
    except Exception as e:
        return []  # fail-safe: empty list if site unreachable

    soup = BeautifulSoup(response.text, "html.parser")
    notices = []

    # Homepage ke notification links generally <a> tags hote hain jinke href me "/file/" ya
    # "/view-notice-list/" aata hai — inhi ko target karte hain
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        title = a_tag.get_text(strip=True)
        if title and ("/file/" in href or "/view-notice-list/" in href):
            if not href.startswith("http"):
                href = MMHAPU_HOME_URL.rstrip("/") + href
            notices.append({"title": title, "link": href})
        if len(notices) >= MAX_NOTICES:
            break

    return notices


def refresh_cache() -> dict:
    """Scrapes fresh data and saves to cache with timestamp."""
    notices = scrape_notifications()
    cache = {
        "last_updated": datetime.now().isoformat(),
        "notices": notices,
    }
    with open(NOTIF_CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)
    return cache


def load_cache() -> dict:
    if not os.path.exists(NOTIF_CACHE_PATH):
        return {"last_updated": None, "notices": []}
    with open(NOTIF_CACHE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_notifications(force_refresh: bool = False, max_age_hours: int = 6) -> list[dict]:
    """
    Returns cached notifications. Auto-refreshes if cache is missing/stale
    (older than max_age_hours) or force_refresh is True.
    """
    cache = load_cache()

    needs_refresh = force_refresh or cache["last_updated"] is None
    if not needs_refresh and cache["last_updated"]:
        last_updated = datetime.fromisoformat(cache["last_updated"])
        if datetime.now() - last_updated > timedelta(hours=max_age_hours):
            needs_refresh = True

    if needs_refresh:
        cache = refresh_cache()

    return cache["notices"]