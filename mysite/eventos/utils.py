    
from mailersend import emails
from django.conf import settings

def send_mailer_send_email(to_emails, subject, content):
    mailer = emails.NewEmail(settings.MAILERSEND_API_KEY)

    email_params = {
        "from": "your_email@example.com",  # Seu e-mail registrado no MailerSend
        "from_name": "Your Name",
        # "to": to_emails,
        "to": 'eoviezzer@ucs.br',
        "subject": subject,
        "text": content,
        "html": f"<p>{content}</p>"
    }

    response = mailer.send(email_params)
    return response