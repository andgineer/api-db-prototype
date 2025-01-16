from typing import Any, Dict, List, Optional

import boto3
from botocore.exceptions import ClientError, NoCredentialsError

import settings
from journaling import log

MAX_MESSAGES = 10  # Amazon limits max number of requested messages
CHARSET = "UTF-8"


def aws_session() -> Any:
    """AWS Session."""
    return boto3

    # Authorization by local credentials. Not necessary if AWS box we run on has appropriate IAM role.
    # return boto3.Session(
    #     aws_access_key_id=settings.config.aws_key_id,
    #     aws_secret_access_key=settings.config.aws_secret_key,
    # )


def ses() -> Any:
    """Amazon simple email service."""
    assert settings.config
    return aws_session().client("ses", region_name=settings.config.aws_region)


def send_email(
    recipients: List[Any], subject: str, html: Optional[str] = None, text: Optional[str] = None
) -> None:
    """Send email via Amazon SES."""
    try:
        message: Dict[str, Dict[str, Any]] = {
            "Body": {},
            "Subject": {
                "Charset": CHARSET,
                "Data": subject,
            },
        }
        if html:
            message["Body"]["Html"] = {
                "Charset": CHARSET,
                "Data": html,
            }
        if text:
            message["Body"]["Text"] = {
                "Charset": CHARSET,
                "Data": text,
            }
        response = ses().send_email(
            Destination={
                "ToAddresses": recipients,
            },
            Message=message,
            Source=settings.config.sender_email,  # type: ignore
            # ConfigurationSetName=CONFIGURATION_SET,
        )
    except NoCredentialsError:
        log.error(
            "Error sending email: Amazon engine unable to locate credentials. May be we are running in dev/test environment."
        )
    except ClientError as e:
        log.error(e.response["Error"]["Message"])
    else:
        log.info("Email sent! Message ID:")
        log.debug(response["MessageId"])


def sqs() -> Any:
    """Amazon simple queue service."""
    assert settings.config
    return aws_session().client("sqs", region_name=settings.config.aws_region)


def queue_url() -> str:
    """URL of the queue we use in our application."""
    assert settings.config
    return sqs().get_queue_url(QueueName=settings.config.aws_queue)["QueueUrl"]  # type: ignore


def queue() -> Any:
    """Specific queue we use in our application."""
    assert settings.config
    return sqs().get_queue_by_name(QueueName=settings.config.aws_queue)  # type: ignore


def queue_messages_list() -> list[Dict[str, Any]]:
    """List of messages in the queue."""
    result = []
    while True:
        messages = queue().receive_messages(
            MaxNumberOfMessages=MAX_MESSAGES,
            VisibilityTimeout=1,
            WaitTimeSeconds=1,
        )
        if len(messages) == 0:
            break
        result.extend(messages)
    return result


def get_queue_message() -> Optional[Dict[str, Any]]:
    """Get one message from the queue."""
    messages = sqs().receive_message(
        QueueUrl=queue_url(),
        MaxNumberOfMessages=1,
        VisibilityTimeout=1,
        WaitTimeSeconds=1,
    )
    if "Messages" not in messages or len(messages["Messages"]) == 0:
        return None
    log.debug(f"Got SQS messages: {messages['Messages']}")
    return messages["Messages"][0]  # type: ignore


def send_queue_message(body: str) -> None:
    """Send message to the queue."""
    response = sqs().send_message(
        QueueUrl=queue_url(), DelaySeconds=10, MessageAttributes={}, MessageBody=body
    )
    log.debug(f'Sent SQS message "{body}",\n\nresponse: {response}')


def delete_queue_message(message: Dict[str, Any]) -> None:
    """Delete message from the queue."""
    log.debug(f"Delete message {message}")
    sqs().delete_message(
        QueueUrl=queue_url(),
        ReceiptHandle=message["ReceiptHandle"],
    )


if __name__ == "__main__":
    settings.config = settings.ConfigProd()
    send_email(["support@example.com"], "Some subject", text="Some text")
