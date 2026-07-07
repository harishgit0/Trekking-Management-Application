from flask_mail import Message
from application import mail


def send_email(subject, recipients, body=None, html=None):
    """
    Send an email with optional HTML content.
    """
    msg = Message(
        subject=subject,
        recipients=recipients
    )

    if body:
        msg.body = body

    if html:
        msg.html = html

    mail.send(msg)