# -*- coding: utf-8 -*-
import os
import sqlite3

# 採用絕對與相對雙重備援匯入，確保在 CI/CD 與本機環境皆能正確載入 vector_memory
try:
    from core.vector_memory import VectorMemory
except ModuleNotFoundError:
    from .vector_memory import VectorMemory

class MemoryManager:
    def __init__(self, db_path: str = "himeko_memory.db"):
        self.db_path = db_path
        self.vector_memory = VectorMemory()
        self._init_db()

    def _init_db(self):
        """初始化 SQLite 資料庫，建立歷史記憶對話表與索引標籤"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversation_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                role TEXT NOT NULL,
                content TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def add_memory(self, role: str, content: str):
        """新增記憶至資料庫與向量索引"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO conversation_history (role, content)
            VALUES (?, ?)
        ''', (role, content))
        conn.commit()
        conn.close()
        
        # 同步向向量記憶庫寫入索引
        self.vector_memory.add_vector(content, metadata={"role": role})

    def get_recent_history(self, limit: int = 5):
        """取得最近的對話歷史紀錄"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT role, content FROM conversation_history
            ORDER BY id DESC LIMIT ?
        ''', (limit,))
        rows = cursor.fetchall()
        conn.close()
        return [{"role": row[0], "content": row[1]} for row in reversed(rows)]
