from app import create_app
from app.utils.telegram import send_telegram_message
from flask import current_app

app = create_app()

with app.app_context():
    chat_id = current_app.config.get('TELEGRAM_ADMIN_CHAT_ID')
    ok = send_telegram_message(chat_id, 'Overview+ Telegram test message ✅')
    print('OK' if ok else 'FAILED')