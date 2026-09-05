import unittest
from core.gestalt_engine import GestaltEngine

class TestGestaltEngine(unittest.TestCase):
    def test_process_intent_approved(self):
        engine = GestaltEngine(capacity=3)
        # 測試合規與意圖對齊合成
        result = engine.process_intent("Hello Himeko OS", {"age": 25})
        self.assertEqual(result["status"], "approved")
        self.assertEqual(len(result["violations"]), 0)
        self.assertIsNotNone(result["gestalt_intent"])
        self.assertEqual(result["gestalt_intent"]["primary_focus"], "Hello Himeko OS")

    def test_process_intent_rejected(self):
        engine = GestaltEngine(capacity=3)
        # 註冊一條會違規的測試規則
        engine.constitution.add_rule("RULE_AGE", "Must be 18+", lambda ctx: ctx.get("age", 0) >= 18)
        
        # 測試違規被拒絕的情況
        result = engine.process_intent("Test input", {"age": 16})
        self.assertEqual(result["status"], "rejected")
        self.assertIn("RULE_AGE", result["violations"])
        self.assertIsNone(result["gestalt_intent"])

if __name__ == '__main__':
    unittest.main()
