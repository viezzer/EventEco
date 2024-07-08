    
from mailersend import emails
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def send_mailer_send_email(to_emails, subject, content):
    mailer = emails.NewEmail(settings.MAILERSEND_API_KEY)

    email_params = {
        "from": "trial-351ndgwy22qlzqx8.mlsender.net",  # Seu e-mail registrado no MailerSend
        "from_name": "Your Name",
        # "to": to_emails,
        "to": ['eoviezzer@ucs.br'],
        "subject": subject,
        "text": content,
        "html": f"<p>{content}</p>"
    }

    response = mailer.send(email_params)
    return response

def send_test_email(to_emails, subject, content):
    print(to_emails)
    email_from = settings.EMAIL_HOST_USER
    to_emails = ['eoviezzer@ucs.br', 'ppschneider@ucs.br', 'vhsantos@ucs.br']

    for email in to_emails:
        # Criar o email
        email_message = EmailMultiAlternatives(
            subject=subject,
            body=content,  # Texto sem formatação (plain text)
            from_email=email_from,
            to=[email]
        )

        # Anexar a versão HTML do email
        email_message.attach_alternative(content, "text/html")

        # Enviar o email
        email_message.send()
