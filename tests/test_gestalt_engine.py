import unittest
from core.gestalt_engine import GestaltEngine

class TestGestaltEngine(unittest.TestCase):
    def test_initialization(self):
        engine = GestaltEngine()
        self.assertEqual(engine.state, "initialized")

if __name__ == '__main__':
    unittest.main()
