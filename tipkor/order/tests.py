from unittest.mock import Mock, patch

from django.test import SimpleTestCase

from order.sender import send_email_safely


class SendEmailSafelyTests(SimpleTestCase):
    @patch('order.sender.send_email', return_value=(True, True))
    def test_returns_true_when_email_is_sent(self, send_email):
        order = Mock(id=42)

        result = send_email_safely('client@example.com', order)

        self.assertTrue(result)
        send_email.assert_called_once_with('client@example.com', order)

    @patch('order.sender.send_email', side_effect=OSError('SMTP unavailable'))
    def test_email_error_does_not_break_order_flow(self, send_email):
        order = Mock(id=42)

        result = send_email_safely('client@example.com', order)

        self.assertFalse(result)
        send_email.assert_called_once_with('client@example.com', order)

    @patch('order.sender.send_email', return_value=(False, True))
    def test_empty_client_email_still_sends_order_notification(self, send_email):
        order = Mock(id=42)

        result = send_email_safely('', order)

        self.assertTrue(result)
        send_email.assert_called_once_with('', order)
