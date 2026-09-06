# -*- coding: utf-8 -*-
import sys
import os
import traceback

# 取得當前目錄與上層目錄
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)

# 將當前目錄與上層目錄優先加入 sys.path
for path in [CURRENT_DIR, PARENT_DIR]:
    if path not in sys.path:
        sys.path.insert(0, path)

try:
    from core.gestalt_engine import GestaltEngine
    print("[Success] Core modules imported successfully!")
except Exception as e:
    print("=== Detailed Import Error ===")
    traceback.print_exc()
    sys.exit(1)

def main():
    print("Initializing Himeko Cognitive OS...")
    engine = GestaltEngine()
    print("Himeko Cognitive OS Core successfully loaded.")

if __name__ == "__main__":
    main()
