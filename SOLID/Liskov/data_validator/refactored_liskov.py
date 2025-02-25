from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from datetime import datetime


class ValidationResult:
    """
    Represents the result of a validation operation.
    Provides a consistent interface for all validator types.
    """

    def __init__(self,
                 is_valid: bool,
                 errors: Optional[List[str]] = None):
        self.is_valid = is_valid
        self.errors = errors or []
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

    @abstractmethod
    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        """
        Validates the provided data and returns a ValidationResult.

        Args:
            data: Dictionary containing the data to validate

        Returns:
            ValidationResult object containing validation status and details
        """
        pass


class EmailValidator(DataValidator):
    """
    Validates email format and related requirements.
    Follows LSP by maintaining the same contract as the base class.
    """

    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        errors = []

        # Check if email field exists
        if 'email' not in data:
            errors.append("Email field is missing")
            return ValidationResult(False, errors)

        email = str(data['email'])

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
        errors = []

        if 'age' not in data:
            errors.append("Age field is missing")
            return ValidationResult(False, errors)

        try:
            age = int(data['age'])

            if age < 0:
                errors.append("Age cannot be negative")
            elif age < 18:
                errors.append("Age must be 18 or above")

        except ValueError:
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
        errors = []

        if 'password' not in data:
            errors.append("Password field is missing")
            return ValidationResult(False, errors)

        password = str(data['password'])

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

    def __init__(self):
        self.validators: List[DataValidator] = []

    def add_validator(self, validator: DataValidator) -> None:
        """
        Adds a validator to the test suite.
        Any validator subclass can be added, demonstrating LSP.
        """
        self.validators.append(validator)

    def run_validations(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Runs all validators on the provided data.
        Shows how validators can be used interchangeably.
        """
        results = []
        for validator in self.validators:
            validator_name = validator.__class__.__name__
            result = validator.validate(data)
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

    # Create validator suite
    runner = ValidationTestRunner()
    runner.add_validator(EmailValidator())
    runner.add_validator(AgeValidator())
    runner.add_validator(PasswordValidator())

    # Run validations
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
