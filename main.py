# -*- coding: utf-8 -*-
import sys
import os

# 動態將當前 main.py 所在的目錄加入系統路徑，徹底解決 CI/CD 的 ModuleNotFoundError 問題
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from core.gestalt_engine import GestaltEngine

def main():
    print("Initializing Himeko Cognitive OS...")
    engine = GestaltEngine()
    print("Himeko Cognitive OS Core successfully loaded.")

if __name__ == "__main__":
    main()
