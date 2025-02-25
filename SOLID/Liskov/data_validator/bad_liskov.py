from typing import Any, Dict

# Bad example - Violating LSP
# ===============================


class DataValidator:
    def validate(self, data: Dict[str, Any]) -> bool:
        # Base validation logic
        return True


class EmailValidator(DataValidator):
    def validate(self, data: Dict[str, str]) -> bool:  # ❌ LSP violation: more restrictive input type
        if 'email' not in data:
            raise ValueError("Email field required")  # ❌ LSP violation: adds new exceptions
        return '@' in data['email']


class AgeValidator(DataValidator):
    def validate(self, data: Any) -> Dict[str, bool]:  # ❌ LSP violation: different return type
        return {'valid': isinstance(data.get('age'), int) and data['age'] >= 18}


