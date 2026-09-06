# -*- coding: utf-8 -*-
import sys
import os
import traceback

# 強制將專案目錄與當前工作目錄加入 sys.path 最前端
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

print(f"[Debug] Current Working Dir: {os.getcwd()}")
print(f"[Debug] BASE_DIR: {BASE_DIR}")
print(f"[Debug] Directory Contents: {os.listdir(BASE_DIR)}")

if os.path.exists(os.path.join(BASE_DIR, "core")):
    print(f"[Debug] core/ Contents: {os.listdir(os.path.join(BASE_DIR, 'core'))}")

try:
    print("[Debug] Testing import core...")
    import core
    print("[Debug] Testing import core.gestalt_engine...")
    import core.gestalt_engine
    from core.gestalt_engine import GestaltEngine
    print("[Success] GestaltEngine imported successfully!")
except Exception as e:
    print("=== Detailed Import Error Stacktrace ===")
    traceback.print_exc()
    sys.exit(1)

def main():
    print("Initializing Himeko Cognitive OS...")
    engine = GestaltEngine()
    print("Himeko Cognitive OS Core successfully loaded.")

if __name__ == "__main__":
    main()
