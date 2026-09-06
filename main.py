# -*- coding: utf-8 -*-
import sys
import os
import traceback

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

try:
    from core.gestalt_engine import GestaltEngine
    print("Successfully imported GestaltEngine!")
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
