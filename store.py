import json

from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DB_DIR = ROOT / "db"

def _get_user_data_file(username):
    """Get the user-specific data file path"""
    return DB_DIR / username / "study.json"

def default_data():
    return {
        "student_name": "",
        "daily_budget": 0.0,
        "mood": "Okay",
        "tomorrow_needs": "",
        "tasks": [],
        "expenses": [],
        "history": [],
        "level": 1,
        "coins": 0,
        "last_updated": ""
    }


def _normalize_data(data):
    normalized = default_data()
    normalized.update(data or {})

    # Support legacy key name while keeping a single canonical field.
    if not normalized.get("tomorrow_needs") and normalized.get("tomorrow_tasks"):
        normalized["tomorrow_needs"] = normalized.get("tomorrow_tasks", "")

    if isinstance(normalized.get("student_name"), list):
        normalized["student_name"] = ""
    if isinstance(normalized.get("mood"), list):
        normalized["mood"] = "Okay"
    if isinstance(normalized.get("last_updated"), list):
        normalized["last_updated"] = ""
    if not isinstance(normalized.get("tasks"), list):
        normalized["tasks"] = []
    if not isinstance(normalized.get("expenses"), list):
        normalized["expenses"] = []
    if not isinstance(normalized.get("history"), list):
        normalized["history"] = []

    try:
        normalized["daily_budget"] = float(normalized.get("daily_budget", 0) or 0)
    except (TypeError, ValueError):
        normalized["daily_budget"] = 0.0

    try:
        normalized["coins"] = int(normalized.get("coins", 0) or 0)
    except (TypeError, ValueError):
        normalized["coins"] = 0

    try:
        normalized["level"] = int(normalized.get("level", 1) or 1)
    except (TypeError, ValueError):
        normalized["level"] = 1

    return normalized

def load_data(username=None):
    """Load user data. If username is None, uses default shared data file for backwards compatibility."""
    if username is None:
        # Backwards compatibility: use old shared data file
        data_file = DB_DIR / "study.json"
    else:
        data_file = _get_user_data_file(username)
    
    if not data_file.exists():
        data = default_data()
        data_file.parent.mkdir(parents=True, exist_ok=True)
        data_file.write_text(json.dumps(data, indent=4), encoding="utf-8")
        return data
    
    try:
        data = json.loads(data_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        data = default_data()
        data_file.write_text(json.dumps(data, indent=4), encoding="utf-8")
        return data

    normalized = _normalize_data(data)
    # Persist normalized values so future runs stay consistent.
    data_file.write_text(json.dumps(normalized, indent=4), encoding="utf-8")
    return normalized


def save_data(data, username=None):
    """Save user data. If username is None, uses default shared data file for backwards compatibility."""
    if username is None:
        # Backwards compatibility: use old shared data file
        data_file = DB_DIR / "study.json"
    else:
        data_file = _get_user_data_file(username)
    
    data_file.parent.mkdir(parents=True, exist_ok=True)
    normalized = _normalize_data(data)
    normalized["last_updated"] = datetime.now().isoformat(timespec="seconds")
    data_file.write_text(json.dumps(normalized, indent=4), encoding="utf-8")