import sqlite3
from typing import List, Dict, Any

class MemoryStore:
    def __init__(self, db_path: str = "cognitive_memory.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS long_term_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                metadata TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    def save_memory(self, content: str, metadata: str = ""):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO long_term_memory (content, metadata) VALUES (?, ?)",
            (content, metadata)
        )
        conn.commit()
        conn.close()

    def query_memories(self, limit: int = 5) -> List[Dict[str, Any]]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, content, metadata, timestamp FROM long_term_memory ORDER BY id DESC LIMIT ?",
            (limit,)
        )
        rows = cursor.fetchall()
        conn.close()

        return [
            {"id": r[0], "content": r[1], "metadata": r[2], "timestamp": r[3]}
            for r in rows
        ]
