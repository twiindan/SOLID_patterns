# After applying Dependency Injection
# Loosely coupled, testable implementation
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict
import requests
from datetime import datetime


@dataclass
class PaymentRequest:
    """
    Data class that encapsulates payment request information.
    Using dataclasses provides a clean way to represent data structures.
    """
    amount: float
    email: str
    card_number: str


@dataclass
class NotificationRequest:
    """
    Data class that encapsulates notification request information.
    Separates notification data from payment data.
    """
    to: str
    subject: str
    message: str


# DEPENDENCY INJECTION PATTERN: Abstract interfaces
# These abstract classes define contracts that implementations must follow
# This enables substituting different implementations without changing client code
class PaymentGateway(ABC):
    """
    Abstract interface for payment gateway services.
    Any payment gateway implementation must implement this interface.
    """

    @abstractmethod
    def process(self, payment: PaymentRequest) -> Dict:
        pass


class NotificationService(ABC):
    """
    Abstract interface for notification services.
    Any notification service implementation must implement this interface.
    """

    @abstractmethod
    def send_notification(self, notification: NotificationRequest) -> bool:
        pass


class PaymentLogger(ABC):
    """
    Abstract interface for payment logging services.
    Any payment logger implementation must implement this interface.
    """

    @abstractmethod
    def log_payment(self, email: str, amount: float) -> None:
        pass


# Concrete implementations
class StripePaymentGateway(PaymentGateway):
    """
    Concrete implementation of the PaymentGateway interface using Stripe.
    Follows the interface contract defined by PaymentGateway.
    """

    def __init__(self, api_url: str):
        # Configuration is injected through constructor
        self.api_url = api_url

    def process(self, payment: PaymentRequest) -> Dict:
        response = requests.post(
            f"{self.api_url}/process",
            json={
                "amount": payment.amount,
                "email": payment.email,
                "card_number": payment.card_number
            }
        )
        return response.json()


class EmailNotificationService(NotificationService):
    """
    Concrete implementation of the NotificationService interface using email.
    Follows the interface contract defined by NotificationService.
    """

    def __init__(self, api_url: str):
        # Configuration is injected through constructor
        self.api_url = api_url

    def send_notification(self, notification: NotificationRequest) -> bool:
        response = requests.post(
            f"{self.api_url}/send",
            json={
                "to": notification.to,
                "subject": notification.subject,
                "message": notification.message
            }
        )
        return response.status_code == 200


class FilePaymentLogger(PaymentLogger):
    """
    Concrete implementation of the PaymentLogger interface using file storage.
    Follows the interface contract defined by PaymentLogger.
    """

    def __init__(self, filename: str):
        # Configuration is injected through constructor
        self.filename = filename

    def log_payment(self, email: str, amount: float) -> None:
        with open(self.filename, "a") as f:
            f.write(f"{datetime.now()}: Payment processed for {email} - ${amount}\n")


# Main service using dependency injection
class PaymentProcessor:
    """
    Main service class that processes payments.

    DEPENDENCY INJECTION PATTERN:
    - Dependencies are injected through constructor
    - Class depends on abstractions (interfaces), not concrete implementations
    - Dependencies can be easily substituted (e.g., for testing)
    """

    def __init__(
            self,
            payment_gateway: PaymentGateway,
            notification_service: NotificationService,
            payment_logger: PaymentLogger
    ):
        # Dependencies are injected through constructor
        self.payment_gateway = payment_gateway
        self.notification_service = notification_service
        self.payment_logger = payment_logger

    def process_payment(self, payment: PaymentRequest) -> Dict:
        # Process payment
        result = self.payment_gateway.process(payment)

        if result.get("status") == "success":
            # Send notification
            notification = NotificationRequest(
                to=payment.email,
                subject="Payment Processed",
                message=f"Your payment of ${payment.amount} was processed"
            )
            self.notification_service.send_notification(notification)

            # Log payment
            self.payment_logger.log_payment(payment.email, payment.amount)

        return result


# Example test using mock objects
from unittest.mock import Mock


def test_successful_payment():
    """
    Unit test that demonstrates a key benefit of dependency injection:
    - Easy mocking of dependencies for isolated testing
    - No real external services are called during testing
    """
    # Create mock objects
    mock_gateway = Mock(spec=PaymentGateway)
    mock_notification = Mock(spec=NotificationService)
    mock_logger = Mock(spec=PaymentLogger)

    # Configure mock behavior
    mock_gateway.process.return_value = {"status": "success", "transaction_id": "123"}
    mock_notification.send_notification.return_value = True

    # Create processor with mock dependencies
    processor = PaymentProcessor(
        payment_gateway=mock_gateway,
        notification_service=mock_notification,
        payment_logger=mock_logger
    )

    # Test payment processing
    payment = PaymentRequest(
        amount=100.0,
        email="test@example.com",
        card_number="4111111111111111"
    )

    result = processor.process_payment(payment)

    # Verify interactions
    assert result["status"] == "success"
    mock_gateway.process.assert_called_once_with(payment)
    mock_notification.send_notification.assert_called_once()
    mock_logger.log_payment.assert_called_once_with("test@example.com", 100.0)


# Example usage with real implementations
def main():
    """
    Example of using the PaymentProcessor with real implementations.
    Shows how dependencies are created and injected.
    """
    # Create real implementations
    payment_gateway = StripePaymentGateway("https://payment-gateway.com/api")
    notification_service = EmailNotificationService("https://notification-service.com/api")
    payment_logger = FilePaymentLogger("payments.log")

    # Create processor with real dependencies
    processor = PaymentProcessor(
        payment_gateway=payment_gateway,
        notification_service=notification_service,
        payment_logger=payment_logger
    )

    # Process a payment
    payment = PaymentRequest(
        amount=99.99,
        email="customer@example.com",
        card_number="4111111111111111"
    )

    result = processor.process_payment(payment)
    print(f"Payment result: {result}")
