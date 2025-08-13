import smtplib
from email.mime.text import MIMEText
from flask import current_app


def send_email(to_email: str, subject: str, html_body: str) -> bool:
    server = current_app.config.get('SMTP_SERVER')
    port = current_app.config.get('SMTP_PORT', 587)
    user = current_app.config.get('SMTP_USER')
    password = current_app.config.get('SMTP_PASS')
    email_from = current_app.config.get('EMAIL_FROM', user)
    debug = str(current_app.config.get('SMTP_DEBUG', '0')).lower() in ('1','true','yes')
    if not server or not user or not password:
        current_app.logger.error('SMTP not configured (server/user/pass missing)')
        return False

    msg = MIMEText(html_body, 'html')
    msg['Subject'] = subject
    msg['From'] = email_from
    msg['To'] = to_email

    try:
        with smtplib.SMTP(server, port, timeout=20) as smtp:
            if debug:
                smtp.set_debuglevel(1)
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(user, password)
            smtp.sendmail(email_from, [to_email], msg.as_string())
        return True
    except Exception as e:
        try:
            current_app.logger.exception('SMTP send failed')
        except Exception:
            pass
        print(f'SMTP ERROR: {e}')
        return False