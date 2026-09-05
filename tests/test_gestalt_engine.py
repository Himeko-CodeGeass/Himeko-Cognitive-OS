import sys
import os

# 強制將專案根目錄加入 Python 搜尋路徑
sys.path.insert(0, os.path.abspath('.'))


import unittest
from core.gestalt_engine import GestaltEngine

class TestGestaltEngine(unittest.TestCase):
    def test_initialization(self):
        engine = GestaltEngine()
        self.assertEqual(engine.state, "initialized")

if __name__ == '__main__':
    unittest.main()
