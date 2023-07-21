import pytest
from unittest.mock import MagicMock, patch
from cloud_services import send_email, get_queue_message, send_queue_message, delete_queue_message
import botocore.exceptions
import settings


@pytest.fixture(autouse=True)
def setup_config():
    settings.config.sender_email = 'test@example.com'

def test_send_email():
    with patch('cloud_services.ses') as mock_ses:
        mock_ses.return_value.send_email.return_value = {"MessageId": "123456789"}
        recipients = ["test@example.com"]
        subject = "Test"
        html = "<p>This is a test email</p>"
        text = "This is a test email"

        send_email(recipients, subject, html, text)

        mock_ses.return_value.send_email.assert_called_once()
        assert mock_ses.return_value.send_email.call_args[1]['Message']['Body']['Html']['Data'] == html
        assert mock_ses.return_value.send_email.call_args[1]['Message']['Body']['Text']['Data'] == text


def test_get_queue_message():
    with patch('cloud_services.sqs') as mock_sqs, patch('cloud_services.queue_url') as mock_queue_url:
        mock_sqs.return_value.receive_message.return_value = {"Messages": [{"MessageId": "123456789", "ReceiptHandle": "handle"}]}
        mock_queue_url.return_value = "https://queue.amazonaws.com/123456789/test"

        message = get_queue_message()

        mock_sqs.return_value.receive_message.assert_called_once()
        assert message['MessageId'] == "123456789"


def test_send_queue_message():
    with patch('cloud_services.sqs') as mock_sqs, patch('cloud_services.queue_url') as mock_queue_url:
        mock_sqs.return_value.send_message.return_value = {}
        mock_queue_url.return_value = "https://queue.amazonaws.com/123456789/test"
        body = "This is a test message"

        send_queue_message(body)

        mock_sqs.return_value.send_message.assert_called_once()
        assert mock_sqs.return_value.send_message.call_args[1]['MessageBody'] == body


def test_delete_queue_message():
    with patch('cloud_services.sqs') as mock_sqs, patch('cloud_services.queue_url') as mock_queue_url:
        mock_queue_url.return_value = "https://queue.amazonaws.com/123456789/test"
        message = {"MessageId": "123456789", "ReceiptHandle": "handle"}

        delete_queue_message(message)

        mock_sqs.return_value.delete_message.assert_called_once()
        assert mock_sqs.return_value.delete_message.call_args[1]['ReceiptHandle'] == "handle"
