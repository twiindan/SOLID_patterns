from typing import Any, Dict


# Bad example - Violating LSP
# ===============================


class DataValidator:
    # Base class that establishes a contract:
    # - Input: Takes a dictionary with string keys and any values
    # - Output: Returns a boolean indicating validity
    # - Behavior: Should not raise unexpected exceptions

    def validate(self, data: Dict[str, Any]) -> bool:
        # Base validation logic
        # This implies that all subclasses should:
        # 1. Accept any dictionary with string keys
        # 2. Return a simple boolean
        # 3. Not raise exceptions during normal operation
        return True


class EmailValidator(DataValidator):
    def validate(self, data: Dict[str, str]) -> bool:  # ❌ LSP violation: more restrictive input type
        # VIOLATION #1: Parameter type is more restrictive
        # The base class accepts Dict[str, Any], but this only accepts Dict[str, str]
        # This means code that passes valid parameters to the base class might fail with this subclass

        if 'email' not in data:
            raise ValueError("Email field required")  # ❌ LSP violation: adds new exceptions
            # VIOLATION #2: Introduces unexpected exceptions
            # The base class doesn't raise exceptions, but this subclass does
            # This breaks client code that doesn't expect exceptions from validate()

        return '@' in data['email']
        # The return type (bool) is consistent with the base class - this part is correct


class AgeValidator(DataValidator):
    def validate(self, data: Any) -> Dict[str, bool]:  # ❌ LSP violation: different return type
        # VIOLATION #1: Parameter type changed completely
        # Base class expects Dict[str, Any], but this accepts Any
        # While this is more permissive (not more restrictive), it still breaks the interface contract

        # VIOLATION #2: Return type changed completely
        # Base class returns bool, but this returns Dict[str, bool]
        # Client code expecting a boolean will break when it receives a dictionary

        return {'valid': isinstance(data.get('age'), int) and data['age'] >= 18}

# Summary of LSP violations in this code:
# 1. EmailValidator uses a more restrictive parameter type (contravariance violation)
# 2. EmailValidator introduces exceptions not present in the base class (behavioral violation)
# 3. AgeValidator changes both parameter and return types (type signature violation)
#
# These violations mean that code written to work with DataValidator cannot reliably
# work with its subclasses, breaking the fundamental principle of substitutability.
