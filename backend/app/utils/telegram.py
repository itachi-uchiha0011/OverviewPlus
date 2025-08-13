import requests
from flask import current_app

def send_telegram_message(chat_id: str, text: str) -> bool:
    token = current_app.config.get('TELEGRAM_BOT_TOKEN')
    if not token or not chat_id:
        return False
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    try:
        r = requests.post(url, json={'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}, timeout=10)
        return r.status_code == 200
    except Exception:
        return False