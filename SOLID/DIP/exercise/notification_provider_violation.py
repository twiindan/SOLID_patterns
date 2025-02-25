import smtplib
from twilio.rest import Client


class NotificationTest:
    def __init__(self):
        # Direct dependency on concrete implementations
        self.email_server = smtplib.SMTP('smtp.gmail.com', 587)
        self.email_server.starttls()
        self.email_server.login('test@example.com', 'password')

        # Direct dependency on Twilio
        self.sms_client = Client('account_sid', 'auth_token')

    def test_send_email_notification(self):
        # Test directly coupled to SMTP implementation
        message = "Test notification"
        self.email_server.sendmail(
            'from@example.com',
            'to@example.com',
            message
        )

        # Basic assertion
        assert self.email_server.noop()[0] == 250

    def test_send_sms_notification(self):
        # Test directly coupled to Twilio implementation
        message = self.sms_client.messages.create(
            body="Test SMS",
            from_='+1234567890',
            to='+0987654321'
        )

        # Basic assertion
        assert message.status == 'queued'

    def teardown(self):
        self.email_server.quit()
