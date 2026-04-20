import json

from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
Data_FILE = ROOT / "db" / "study.json"

def default_data():
    return {
        "student_name": [],
        "daily_budget": [],
        "mood": [],
        "tomorrow_tasks": [],
        "tasks": [],
        "expenses": [],
        "level": 1,
        "coins": 0,
        "last_updated": []
    }

def load_data():
    if not Data_FILE.exists():
        data = default_data()
        Data_FILE.parent.mkdir(parents=True, exist_ok=True)
        Data_FILE.write_text(json.dumps(data, indent=4), encoding="utf-8")
        return data
    
    try:
        data = json.loads(Data_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        data = default_data()
        Data_FILE.write_text(json.dumps(data, indent=4), encoding="utf-8")
        return data
    
    base = default_data()
    base.update(data)
    return base
        