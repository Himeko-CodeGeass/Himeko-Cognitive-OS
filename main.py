# -*- coding: utf-8 -*-
import sys
import os

# 確保當前目錄在系統路徑中
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.gestalt_engine import GestaltEngine
from core.heartbeat import HeartbeatEngine
from adapters.local_adapter import LocalAdapter

def main():
    print("==========================================")
    print("   HIMEKO COGNITIVE OS - INITIALIZING      ")
    print("==========================================")

    # 1. 初始化本機記憶與認知引擎
    db_path = "himeko_memory.db"
    engine = GestaltEngine(db_path=db_path)

    # 2. 掛載本機離線轉接器
    adapter = LocalAdapter(mode="deterministic")

    # 3. 啟動自主心跳守護程序 (進行 3 次心跳測試)
    heartbeat = HeartbeatEngine(engine=engine, interval_seconds=1)
    
    print("\n[Main] Launching autonomous heartbeat loop...")
    heartbeat.start_loop(count=3, adapter=adapter)

    print("\n==========================================")
    print("   HIMEKO COGNITIVE OS - RUNTIME SECURE   ")
    print("==========================================")

if __name__ == "__main__":
    main()
