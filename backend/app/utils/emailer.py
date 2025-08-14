import smtplib
from email.mime.text import MIMEText
from flask import current_app


def send_email(to_email: str, subject: str, html_body: str) -> bool:
    server = current_app.config.get('SMTP_SERVER')
    port = current_app.config.get('SMTP_PORT', 587)
    user = current_app.config.get('SMTP_USER')
    password = current_app.config.get('SMTP_PASS')
    email_from = current_app.config.get('EMAIL_FROM', user)
    if not server or not user or not password:
        return False

    msg = MIMEText(html_body, 'html')
    msg['Subject'] = subject
    msg['From'] = email_from
    msg['To'] = to_email

    try:
        with smtplib.SMTP(server, port) as smtp:
            smtp.starttls()
            smtp.login(user, password)
            smtp.sendmail(email_from, [to_email], msg.as_string())
        return True
    except Exception:
        return False