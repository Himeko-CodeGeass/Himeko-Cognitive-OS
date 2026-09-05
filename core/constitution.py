class DynamicConstitution:
    """Dynamic Charter Engine for runtime safety and behavioral constraints."""
    def __init__(self):
        self.rules = []

    def add_rule(self, rule_id, description, validator_func):
        if not rule_id or not validator_func:
            return False
        self.rules.append({
            "id": rule_id,
            "description": description,
            "validator": validator_func
        })
        return True

    def evaluate(self, context):
        violations = []
        for rule in self.rules:
            try:
                # 執行驗證器，若回傳 False 則代表違規
                if not rule["validator"](context):
                    violations.append(rule["id"])
            except Exception:
                violations.append(rule["id"])
        
        return {
            "is_valid": len(violations) == 0,
            "violations": violations
        }

    def clear_rules(self):
        self.rules.clear()
