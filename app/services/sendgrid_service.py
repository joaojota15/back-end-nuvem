from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, To
from app.core.config import settings

def send_reset_email(to_email: str, subject: str, html_content: str):
    message = Mail(
        from_email=(settings.MAIL_FROM, settings.MAIL_FROM_NAME or settings.PROJECT_NAME),
        to_emails=To(to_email),
        subject=subject,
        html_content=html_content
    )
    sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
    response = sg.send(message)
    return response.status_code
