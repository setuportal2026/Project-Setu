# modules/router.py

import json
import os

KRC_JSON_PATH = os.path.join(os.path.dirname(__file__), "krc_data.json")


def load_krc_data() -> dict:
    with open(KRC_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_krc_by_code(krc_code: str, data: dict = None) -> dict | None:
    """Fetch single KRC info by its unique 3-digit code."""
    if data is None:
        data = load_krc_data()
    return data.get(str(krc_code).strip())


def search_krc_by_name(query: str, data: dict = None) -> list[dict]:
    """Search KRCs by (partial) institution name."""
    if data is None:
        data = load_krc_data()
    query = query.lower().strip()
    results = []
    for code, info in data.items():
        if query in info.get("name", "").lower():
            results.append({"krc_code": code, **info})
    return results


def search_krc_by_district(district: str, data: dict = None) -> list[dict]:
    """List all KRCs in a given district (helps find 'nearest' KRC)."""
    if data is None:
        data = load_krc_data()
    district = district.lower().strip()
    results = []
    for code, info in data.items():
        if district in info.get("district", "").lower():
            results.append({"krc_code": code, **info})
    return results


def list_all_districts(data: dict = None) -> list[str]:
    if data is None:
        data = load_krc_data()
    return sorted({info.get("district", "") for info in data.values() if info.get("district")})


def format_krc_card(krc_code: str, info: dict) -> str:
    """Human-readable summary — used in guard.py guidance too."""
    return (
        f"**KRC Code:** {krc_code}\n"
        f"**Institution:** {info.get('name')}\n"
        f"**District:** {info.get('district')}\n"
        f"**Address:** {info.get('address')}\n"
        f"**In-charge:** {info.get('incharge')}\n"
        f"**Contact:** {info.get('contact')}\n"
        f"**Email:** {info.get('email')}"
    )