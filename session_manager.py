import json
import hashlib
import secrets
from datetime import datetime, timedelta
from pathlib import Path

SESSIONS_DIR = Path(__file__).resolve().parent / "db" / "sessions"

def create_session(username):
    """Create a new session for a user and return session ID"""
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
    
    session_id = secrets.token_hex(16)
    session_data = {
        "username": username,
        "created_at": datetime.now().isoformat(),
        "expires_at": (datetime.now() + timedelta(days=7)).isoformat()
    }
    
    session_file = SESSIONS_DIR / f"{session_id}.json"
    session_file.write_text(json.dumps(session_data, indent=2), encoding="utf-8")
    
    return session_id

def validate_session(session_id):
    """Check if session is valid and return username"""
    if not session_id:
        return None
    
    session_file = SESSIONS_DIR / f"{session_id}.json"
    
    if not session_file.exists():
        return None
    
    try:
        session_data = json.loads(session_file.read_text(encoding="utf-8"))
        expires_at = datetime.fromisoformat(session_data["expires_at"])
        
        # Check if session expired
        if datetime.now() > expires_at:
            session_file.unlink()  # Delete expired session
            return None
        
        return session_data["username"]
    except (json.JSONDecodeError, KeyError, ValueError):
        return None

def destroy_session(session_id):
    """Delete a session"""
    session_file = SESSIONS_DIR / f"{session_id}.json"
    if session_file.exists():
        session_file.unlink()

def cleanup_expired_sessions():
    """Remove all expired session files"""
    if not SESSIONS_DIR.exists():
        return
    
    for session_file in SESSIONS_DIR.glob("*.json"):
        try:
            session_data = json.loads(session_file.read_text(encoding="utf-8"))
            expires_at = datetime.fromisoformat(session_data["expires_at"])
            
            if datetime.now() > expires_at:
                session_file.unlink()
        except (json.JSONDecodeError, KeyError, ValueError):
            session_file.unlink()
