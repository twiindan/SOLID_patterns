from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from datetime import datetime


class ValidationResult:
    """
    Represents the result of a validation operation.
    Provides a consistent interface for all validator types.
    """

    # This class is a key part of the LSP-compliant design:
    # 1. It standardizes the return type across all validators
    # 2. It allows for rich information without changing the method signature
    # 3. It supports extension without breaking the contract

    def __init__(self,
                 is_valid: bool,
                 errors: Optional[List[str]] = None):
        self.is_valid = is_valid
        self.errors = errors or []  # Default to empty list if None
        self.timestamp = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the validation result to a dictionary format
        """
        return {
            "is_valid": self.is_valid,
            "errors": self.errors,
            "timestamp": self.timestamp.isoformat()
        }


class DataValidator(ABC):
    """
    Abstract base class for all validators.
    Defines the contract that all validator implementations must follow.
    """

    # Using ABC ensures the contract is explicitly defined and enforced
    # This makes the LSP constraints clear to implementers

    @abstractmethod
    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        """
        Validates the provided data and returns a ValidationResult.

        Args:
            data: Dictionary containing the data to validate

        Returns:
            ValidationResult object containing validation status and details
        """
        # The contract is clearly defined:
        # 1. Input: Dict[str, Any] - accommodates all dictionary data
        # 2. Output: ValidationResult - consistent return type
        # 3. No exceptions in the signature - implementations should handle their own errors
        pass


class EmailValidator(DataValidator):
    """
    Validates email format and related requirements.
    Follows LSP by maintaining the same contract as the base class.
    """

    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        # LSP Compliance:
        # 1. Same parameter type as base class
        # 2. Same return type as base class
        # 3. No unexpected exceptions

        errors = []

        # Check if email field exists
        if 'email' not in data:
            # Instead of throwing an exception (LSP violation),
            # this adds the error to the result
            errors.append("Email field is missing")
            return ValidationResult(False, errors)

        email = str(data['email'])  # Safely convert to string, avoiding type errors

        # Basic email format validation
        if '@' not in email:
            errors.append("Invalid email format: missing @")
        elif '.' not in email.split('@')[1]:
            errors.append("Invalid email format: missing domain")

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
        )


class AgeValidator(DataValidator):
    """
    Validates age-related requirements.
    Maintains LSP compliance with the base validator contract.
    """

    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        # LSP Compliance:
        # 1. Same parameter type as base class
        # 2. Same return type as base class
        # 3. Handles errors within the method instead of unexpected exceptions

        errors = []

        if 'age' not in data:
            errors.append("Age field is missing")
            return ValidationResult(False, errors)

        try:
            # Safely convert and validate age
            age = int(data['age'])  # Handles non-integer input

            if age < 0:
                errors.append("Age cannot be negative")
            elif age < 18:
                errors.append("Age must be 18 or above")

        except ValueError:
            # Gracefully handle type conversion errors
            errors.append("Age must be a valid number")

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
        )


class PasswordValidator(DataValidator):
    """
    Validates password strength and requirements.
    Demonstrates LSP compliance while adding specific validation logic.
    """

    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        # LSP Compliance:
        # 1. Same parameter type as base class
        # 2. Same return type as base class
        # 3. Specialized validation logic without breaking the contract

        errors = []

        if 'password' not in data:
            errors.append("Password field is missing")
            return ValidationResult(False, errors)

        password = str(data['password'])  # Safe conversion

        # Required criteria
        if len(password) < 8:
            errors.append("Password must be at least 8 characters long")
        if not any(c.isupper() for c in password):
            errors.append("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in password):
            errors.append("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in password):
            errors.append("Password must contain at least one number")

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
        )


class ValidationTestRunner:
    """
    Demonstrates LSP in action by working with different validators polymorphically.
    """

    # This class shows the power of LSP:
    # - It can work with any DataValidator without knowing the specific subclass
    # - It treats all validators uniformly through their common interface

    def __init__(self):
        self.validators: List[DataValidator] = []

    def add_validator(self, validator: DataValidator) -> None:
        """
        Adds a validator to the test suite.
        Any validator subclass can be added, demonstrating LSP.
        """
        # Because all validators follow LSP, any can be used here
        self.validators.append(validator)

    def run_validations(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Runs all validators on the provided data.
        Shows how validators can be used interchangeably.
        """
        # This is true polymorphism - treating different types through a common interface
        results = []
        for validator in self.validators:
            validator_name = validator.__class__.__name__
            result = validator.validate(data)  # Same method call works for all validators
            results.append({
                "validator": validator_name,
                **result.to_dict()
            })
        return results


if __name__ == "__main__":
    # Create test data
    test_data = {
        "email": "user.name@example",  # Invalid email
        "age": "17",  # Invalid age
        "password": "short"  # Invalid password
    }

    # Create validator suite - demonstrates LSP in practice
    runner = ValidationTestRunner()
    runner.add_validator(EmailValidator())
    runner.add_validator(AgeValidator())
    runner.add_validator(PasswordValidator())

    # Run validations - all validators are treated uniformly
    print("Running validations...")
    results = runner.run_validations(test_data)

    # Display results
    for result in results:
        print(f"\nValidator: {result['validator']}")
        print(f"Valid: {result['is_valid']}")
        if result['errors']:
            print("Errors:")
            for error in result['errors']:
                print(f"  - {error}")

# Key LSP improvements in this design:
# 1. Consistent parameter and return types across all validators
# 2. Standardized error handling through ValidationResult
# 3. No unexpected exceptions that could break client code
# 4. True polymorphism - all validators can be used interchangeably
# 5. Extensible design - new validator types can be added without changing existing code
