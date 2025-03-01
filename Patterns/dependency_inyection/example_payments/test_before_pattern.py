# Before applying Dependency Injection
# Tightly coupled implementation
import requests
from datetime import datetime


class PaymentProcessor:
    """
    Payment processor without dependency injection.

    ANTI-PATTERN:
    - Hardcoded dependencies and configurations
    - Direct coupling to external services
    - No separation of concerns
    - No abstraction layers
    - Difficult to test
    """

    def __init__(self):
        # PROBLEM: Hardcoded URLs
        # These API endpoints cannot be easily changed or mocked for testing
        self.payment_api_url = "https://payment-gateway.com/api"
        self.notification_service_url = "https://notification-service.com/api"

    def process_payment(self, payment_data):
        """
        Process a payment with tightly coupled dependencies.

        PROBLEMS:
        1. Direct API calls to external services (tight coupling)
        2. Multiple responsibilities in one method (payment, notification, logging)
        3. No abstraction of external services
        4. Hardcoded file path for logging
        5. Impossible to unit test without hitting real external services
        6. No clear separation of concerns
        """
        # PROBLEM: Direct API call to payment gateway
        # Cannot be mocked or substituted for testing
        payment_response = requests.post(
            f"{self.payment_api_url}/process",
            json=payment_data
        )

        if payment_response.status_code == 200:
            # PROBLEM: Direct API call to notification service
            # Cannot be mocked or substituted for testing
            notification_data = {
                "to": payment_data["email"],
                "subject": "Payment Processed",
                "message": f"Your payment of ${payment_data['amount']} was processed"
            }
            requests.post(
                f"{self.notification_service_url}/send",
                json=notification_data
            )

            # PROBLEM: Hardcoded file name and direct file I/O
            # Cannot be mocked or substituted for testing
            with open("payments.log", "a") as f:
                f.write(f"{datetime.now()}: Payment processed for {payment_data['email']}\n")

        return payment_response.json()

    # PROBLEM: No way to unit test this class effectively
    # Any test would need to:
    # 1. Make real HTTP requests to external services
    # 2. Create real log files
    # 3. Handle real payment processing
    # This makes testing slow, fragile, and dependent on external services
