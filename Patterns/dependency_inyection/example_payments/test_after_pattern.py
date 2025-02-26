# After applying Dependency Injection
# Loosely coupled, testable implementation
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict
import requests
from datetime import datetime


@dataclass
class PaymentRequest:
    amount: float
    email: str
    card_number: str


@dataclass
class NotificationRequest:
    to: str
    subject: str
    message: str


class PaymentGateway(ABC):
    @abstractmethod
    def process(self, payment: PaymentRequest) -> Dict:
        pass


class NotificationService(ABC):
    @abstractmethod
    def send_notification(self, notification: NotificationRequest) -> bool:
        pass


class PaymentLogger(ABC):
    @abstractmethod
    def log_payment(self, email: str, amount: float) -> None:
        pass


# Concrete implementations
class StripePaymentGateway(PaymentGateway):
    def __init__(self, api_url: str):
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
    def __init__(self, api_url: str):
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
    def __init__(self, filename: str):
        self.filename = filename

    def log_payment(self, email: str, amount: float) -> None:
        with open(self.filename, "a") as f:
            f.write(f"{datetime.now()}: Payment processed for {email} - ${amount}\n")


# Main service using dependency injection
class PaymentProcessor:
    def __init__(
            self,
            payment_gateway: PaymentGateway,
            notification_service: NotificationService,
            payment_logger: PaymentLogger
    ):
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