# -*- coding: utf-8 -*-
import os
import sqlite3
import hashlib

class VectorMemory:
    def __init__(self, db_path: str = "himeko_vector.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory_vectors (
                id TEXT PRIMARY KEY,
                content TEXT,
                metadata TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def add_memory(self, content: str, metadata: str = ""):
        # 簡易雜湊作為本機輕量唯一識別
        memory_id = hashlib.sha256(content.encode('utf-8')).hexdigest()[:16]
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            OR IGNORE INTO memory_vectors (id, content, metadata)
            VALUES (?, ?, ?)
        ''', (memory_id, content, metadata))
        conn.commit()
        conn.close()
        return f"[VectorMemory] Stored semantic chunk: {memory_id}"

    def search(self, query: str, limit: int = 3) -> list:
        # 本機輕量關鍵字與語義模糊匹配防線（可於後續擴充真正的 Embedding 運算）
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT content, metadata FROM memory_vectors
            WHERE content LIKE ? LIMIT ?
        ''', (f"%{query}%", limit))
        results = cursor.fetchall()
        conn.close()
        return [{"content": r[0], "metadata": r[1]} for r in results]
