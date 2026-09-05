import unittest
from core.gestalt_engine import GestaltEngine

class TestGestaltEngine(unittest.TestCase):
    def test_initialization(self):
        engine = GestaltEngine()
        self.assertEqual(engine.state, "initialized")
        self.assertEqual(len(engine.history), 0)

    def test_process_message(self):
        engine = GestaltEngine()
        result = engine.process("Activate Protocol Himeko")
        self.assertEqual(result, "Processed: Activate Protocol Himeko (Total history: 1)")
        self.assertEqual(len(engine.history), 1)
        self.assertEqual(engine.history[0], "Activate Protocol Himeko")

if __name__ == '__main__':
    unittest.main()
