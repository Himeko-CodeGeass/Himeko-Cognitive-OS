import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.gestalt_engine import GestaltEngine

class TestGestaltEngine(unittest.TestCase):
    def setUp(self):
        self.engine = GestaltEngine(version="v2.0")

    def test_engine_initialization(self):
        self.assertEqual(self.engine.version, "v2.0")

if __name__ == "__main__":
    unittest.main()
