from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Optional
from datetime import datetime


# Domain Models
class NotificationType(Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"


@dataclass
class NotificationContent:
    subject: str
    body: str
    priority: str = "normal"
    metadata: dict = None


@dataclass
class Recipient:
    identifier: str  # email address or phone number
    notification_type: NotificationType
    name: Optional[str] = None


@dataclass
class NotificationResult:
    success: bool
    message_id: str
    timestamp: datetime
    error: Optional[str] = None


# Abstract interfaces
class NotificationProvider(ABC):
    @abstractmethod
    def send_notification(
            self,
            content: NotificationContent,
            recipient: Recipient
    ) -> NotificationResult:
        pass

    @abstractmethod
    def check_status(self, message_id: str) -> str:
        pass

    @abstractmethod
    def close(self) -> None:
        pass


# Concrete implementations
class MockEmailProvider(NotificationProvider):
    def __init__(self):
        self.sent_messages = {}
        self.message_counter = 0

    def send_notification(
            self,
            content: NotificationContent,
            recipient: Recipient
    ) -> NotificationResult:
        if recipient.notification_type != NotificationType.EMAIL:
            raise ValueError("Invalid notification type for email provider")

        self.message_counter += 1
        message_id = f"email_{self.message_counter}"

        self.sent_messages[message_id] = {
            "content": content,
            "recipient": recipient,
            "status": "sent",
            "timestamp": datetime.now()
        }

        return NotificationResult(
            success=True,
            message_id=message_id,
            timestamp=datetime.now()
        )

    def check_status(self, message_id: str) -> str:
        if message_id in self.sent_messages:
            return self.sent_messages[message_id]["status"]
        raise ValueError("Message ID not found")

    def close(self) -> None:
        self.sent_messages.clear()


class MockSMSProvider(NotificationProvider):
    def __init__(self):
        self.sent_messages = {}
        self.message_counter = 0

    def send_notification(
            self,
            content: NotificationContent,
            recipient: Recipient
    ) -> NotificationResult:
        if recipient.notification_type != NotificationType.SMS:
            raise ValueError("Invalid notification type for SMS provider")

        self.message_counter += 1
        message_id = f"sms_{self.message_counter}"

        self.sent_messages[message_id] = {
            "content": content,
            "recipient": recipient,
            "status": "delivered",
            "timestamp": datetime.now()
        }

        return NotificationResult(
            success=True,
            message_id=message_id,
            timestamp=datetime.now()
        )

    def check_status(self, message_id: str) -> str:
        if message_id in self.sent_messages:
            return self.sent_messages[message_id]["status"]
        raise ValueError("Message ID not found")

    def close(self) -> None:
        self.sent_messages.clear()


# Notification Service that uses the abstractions
class NotificationService:
    def __init__(self, providers: dict[NotificationType, NotificationProvider]):
        self.providers = providers

    def send_notification(
            self,
            content: NotificationContent,
            recipient: Recipient
    ) -> NotificationResult:
        provider = self.providers.get(recipient.notification_type)
        if not provider:
            raise ValueError(f"No provider found for {recipient.notification_type}")

        return provider.send_notification(content, recipient)

    def close(self) -> None:
        for provider in self.providers.values():
            provider.close()


# Test class using abstractions
class NotificationTest:
    def __init__(self, notification_service: NotificationService):
        self.notification_service = notification_service

    def test_send_email_notification(self):
        content = NotificationContent(
            subject="Test Email",
            body="This is a test email",
            priority="high"
        )

        recipient = Recipient(
            identifier="test@example.com",
            notification_type=NotificationType.EMAIL,
            name="Test User"
        )

        result = self.notification_service.send_notification(content, recipient)

        assert result.success
        assert result.message_id.startswith("email_")
        assert isinstance(result.timestamp, datetime)

    def test_send_sms_notification(self):
        content = NotificationContent(
            subject="Test SMS",
            body="This is a test SMS",
            priority="normal"
        )

        recipient = Recipient(
            identifier="+1234567890",
            notification_type=NotificationType.SMS
        )

        result = self.notification_service.send_notification(content, recipient)

        assert result.success
        assert result.message_id.startswith("sms_")
        assert isinstance(result.timestamp, datetime)

    def teardown(self):
        self.notification_service.close()


# Example usage
def run_tests():
    # Create providers dictionary with mock implementations
    providers = {
        NotificationType.EMAIL: MockEmailProvider(),
        NotificationType.SMS: MockSMSProvider()
    }

    # Create notification service with providers
    notification_service = NotificationService(providers)

    # Create and run tests
    test = NotificationTest(notification_service)

    try:
        test.test_send_email_notification()
        test.test_send_sms_notification()
        print("All tests passed!")
    finally:
        test.teardown()


if __name__ == "__main__":
    run_tests()
