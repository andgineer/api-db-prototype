import boto3
from botocore.exceptions import ClientError, NoCredentialsError

import settings
from journaling import log

MAX_MESSAGES = 10  # Amazon limits max number of requested messages
CHARSET = "UTF-8"


def aws_session():
    return boto3

    # Authorization by local credentials. Not necessary if AWS box we run on has appropriate IAM role.
    # return boto3.Session(
    #     aws_access_key_id=settings.config.aws_key_id,
    #     aws_secret_access_key=settings.config.aws_secret_key,
    # )


def ses():
    """
    Amazon simple email service
    """
    return aws_session().client("ses", region_name=settings.config.aws_region)


def send_email(recipients: list, subject: str, html: str = None, text: str = None):
    try:
        message = {
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
            Source=settings.config.sender_email,
            # ConfigurationSetName=CONFIGURATION_SET,
        )
    except NoCredentialsError:
        log.error(
            "Error sending email: Amazon engine unable to locate credentials. May be we are running in dev/test environment."
        )
    except ClientError as e:
        log.error(e.response["Error"]["Message"])
    else:
        log.info("Email sent! Message ID:"),
        log.debug(response["MessageId"])


def sqs():
    """
    Amazon simple queue service
    """
    return aws_session().client("sqs", region_name=settings.config.aws_region)


def queue_url():
    return sqs().get_queue_url(QueueName=settings.config.aws_queue)["QueueUrl"]


def queue():
    """
    Specific queue we use in our application
    """
    return sqs().get_queue_by_name(QueueName=settings.config.aws_queue)


def queue_messages_list():
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


def get_queue_message():
    messages = sqs().receive_message(
        QueueUrl=queue_url(),
        MaxNumberOfMessages=1,
        VisibilityTimeout=1,
        WaitTimeSeconds=1,
    )
    if "Messages" not in messages or len(messages["Messages"]) == 0:
        return None
    else:
        log.debug(f'Got SQS messages: {messages["Messages"]}')
        return messages["Messages"][0]


def send_queue_message(body):
    response = sqs().send_message(
        QueueUrl=queue_url(), DelaySeconds=10, MessageAttributes={}, MessageBody=body
    )
    log.debug(f'Sent SQS message "{body}",\n\nresponse: {response}')


def delete_queue_message(message):
    log.debug(f"Delete message {message}")
    sqs().delete_message(
        QueueUrl=queue_url(),
        ReceiptHandle=message["ReceiptHandle"],
    )


if __name__ == "__main__":
    settings.config = settings.ConfigProd()
    send_email(["support@example.com"], "Some subject", text="Some text")
