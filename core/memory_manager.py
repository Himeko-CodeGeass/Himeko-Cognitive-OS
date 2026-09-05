import os

# 確保 core 目錄存在
os.makedirs("core", exist_ok=True)

# 將真實的 SQLite MemoryManager 寫入 core/memory_manager.py
memory_manager_code = """import sqlite3
import os

class MemoryManager:
    def __init__(self, db_path="himeko_memory.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        \"\"\"初始化 SQLite 資料庫與長期記憶資料表\"\"\"
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS long_term_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                intent TEXT NOT NULL,
                response TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
        print(f"[MemoryManager] 資料庫初始化成功，連線路徑: {self.db_path}")

    def save_memory(self, intent: str, response: str):
        \"\"\"將對話意圖與回應寫入長期記憶庫\"\"\"
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO long_term_memory (intent, response)
            VALUES (?, ?)
        ''', (intent, response))
        conn.commit()
        conn.close()
        print(f"[MemoryManager] 已成功持久化記憶 -> 意圖: {intent}")

    def retrieve_recent_memories(self, limit: int = 5):
        \"\"\"從資料庫檢索最近的歷史脈絡以供狀態對齊\"\"\"
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT intent, response, timestamp FROM long_term_memory
            ORDER BY timestamp DESC LIMIT ?
        ''', (limit,))
        rows = cursor.fetchall()
        conn.close()
        
        memories = []
        for row in rows:
            memories.append({"intent": row[0], "response": row[1], "timestamp": row[2]})
        return memories
"""

with open("core/memory_manager.py", "w", encoding="utf-8") as f:
    f.write(memory_manager_code.strip())

print("core/memory_manager.py 寫入成功！")
