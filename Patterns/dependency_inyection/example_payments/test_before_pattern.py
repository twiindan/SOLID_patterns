# Before applying Dependency Injection
# Tightly coupled implementation
import requests
from datetime import datetime


class PaymentProcessor:
    def __init__(self):
        self.payment_api_url = "https://payment-gateway.com/api"
        self.notification_service_url = "https://notification-service.com/api"

    def process_payment(self, payment_data):
        # Process payment through payment gateway
        payment_response = requests.post(
            f"{self.payment_api_url}/process",
            json=payment_data
        )

        if payment_response.status_code == 200:
            # Send notification
            notification_data = {
                "to": payment_data["email"],
                "subject": "Payment Processed",
                "message": f"Your payment of ${payment_data['amount']} was processed"
            }
            requests.post(
                f"{self.notification_service_url}/send",
                json=notification_data
            )

            # Save to database
            with open("payments.log", "a") as f:
                f.write(f"{datetime.now()}: Payment processed for {payment_data['email']}\n")

        return payment_response.json()
