import json
import base64
import hashlib
import hmac
import os
import secrets
from datetime import datetime, timedelta
from pathlib import Path

SESSIONS_DIR = Path(__file__).resolve().parent / "db" / "sessions"
SESSION_TOKEN_SECRET = os.getenv("SAS_SESSION_TOKEN_SECRET", "sas-local-dev-secret")


def create_public_session_token(session_id):
    """Create a signed opaque token for URL use without exposing raw session ID."""
    if not session_id:
        return None

    payload = session_id.encode("utf-8")
    signature = hmac.new(SESSION_TOKEN_SECRET.encode("utf-8"), payload, hashlib.sha256).digest()[:16]
    token_bytes = payload + b"." + signature
    return base64.urlsafe_b64encode(token_bytes).decode("utf-8").rstrip("=")


def parse_public_session_token(token):
    """Validate and decode URL token back to session ID."""
    if not token:
        return None

    try:
        padded = token + "=" * (-len(token) % 4)
        token_bytes = base64.urlsafe_b64decode(padded.encode("utf-8"))
        payload, signature = token_bytes.rsplit(b".", 1)
        expected = hmac.new(SESSION_TOKEN_SECRET.encode("utf-8"), payload, hashlib.sha256).digest()[:16]
        if not hmac.compare_digest(signature, expected):
            return None

        session_id = payload.decode("utf-8")
        if len(session_id) != 32:
            return None
        return session_id
    except Exception:
        return None

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
