from typing import List, Dict

# In-memory placeholder store
MEMORY_DB: List[Dict] = []

def save_memory(user_id: str, text: str):
    MEMORY_DB.append({"user_id": user_id, "text": text})

def get_memories(user_id: str) -> List[Dict]:
    return [m for m in MEMORY_DB if m["user_id"] == user_id]