import unittest
from core.constitution import DynamicConstitution

class TestDynamicConstitution(unittest.TestCase):
    def test_add_rule_and_evaluation(self):
        engine = DynamicConstitution()
        
        # 註冊一條規則：檢查 context 中的 "age" 是否大於或等於 18
        engine.add_rule(
            rule_id="RULE_001",
            description="Age must be at least 18",
            validator_func=lambda ctx: ctx.get("age", 0) >= 18
        )
        
        # 測試合規的情況
        result_valid = engine.evaluate({"age": 20})
        self.assertTrue(result_valid["is_valid"])
        self.assertEqual(len(result_valid["violations"]), 0)
        
        # 測試違規的情況
        result_invalid = engine.evaluate({"age": 16})
        self.assertFalse(result_invalid["is_valid"])
        self.assertIn("RULE_001", result_invalid["violations"])

    def test_clear_rules(self):
        engine = DynamicConstitution()
        engine.add_rule("RULE_002", "Dummy rule", lambda ctx: True)
        self.assertEqual(len(engine.rules), 1)
        
        engine.clear_rules()
        self.assertEqual(len(engine.rules), 0)

if __name__ == '__main__':
    unittest.main()
