"""Simple in-memory conversation storage."""
from typing import Dict, List
from datetime import datetime, timedelta
import uuid


class ConversationMemory:
    """Store conversation history in memory."""
    
    def __init__(self):
        self._sessions: Dict[str, List[Dict]] = {}
        self._max_age = timedelta(hours=2)
    
    def get_or_create_session(self, session_id: str = None) -> str:
        """Get existing session or create new one."""
        if session_id and session_id in self._sessions:
            return session_id
        
        new_session_id = session_id or str(uuid.uuid4())
        self._sessions[new_session_id] = []
        return new_session_id
    
    def add_message(self, session_id: str, role: str, content: str):
        """Add a message to session history."""
        if session_id not in self._sessions:
            self._sessions[session_id] = []
        
        self._sessions[session_id].append({
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def get_history(self, session_id: str, last_n: int = 6) -> List[Dict]:
        """Get last N messages from session."""
        if session_id not in self._sessions:
            return []
        return self._sessions[session_id][-last_n:]
    
    def clear_session(self, session_id: str):
        """Clear a specific session."""
        if session_id in self._sessions:
            del self._sessions[session_id]


memory = ConversationMemory()