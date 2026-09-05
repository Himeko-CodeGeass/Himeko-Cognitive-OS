import unittest
from core.gestalt_engine import GestaltEngine

class TestGestaltEngine(unittest.TestCase):
    def test_process_intent_approved(self):
        engine = GestaltEngine(capacity=3)
        result = engine.process_intent("Hello Himeko OS", {"age": 25})
        self.assertEqual(result["status"], "approved")
        self.assertEqual(len(result["violations"]), 0)
        self.assertIsNotNone(result["gestalt_intent"])
        self.assertEqual(result["gestalt_intent"]["primary_focus"], "Hello Himeko OS")

    def test_process_intent_rejected(self):
        engine = GestaltEngine(capacity=3)
        engine.constitution.add_rule("RULE_AGE", "Must be 18+", lambda ctx: ctx.get("age", 0) >= 18)
        result = engine.process_intent("Test input", {"age": 16})
        self.assertEqual(result["status"], "rejected")
        self.assertIn("RULE_AGE", result["violations"])
        self.assertIsNone(result["gestalt_intent"])

if __name__ == '__main__':
    unittest.main()
