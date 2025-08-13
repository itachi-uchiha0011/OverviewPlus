import secrets
from typing import Optional, Dict

_user_csrf_tokens: Dict[int, str] = {}


def generate_csrf_token() -> str:
	return secrets.token_urlsafe(32)


def set_csrf_token(user_id: int, token: str) -> None:
	_user_csrf_tokens[user_id] = token


def get_csrf_token(user_id: int) -> Optional[str]:
	return _user_csrf_tokens.get(user_id)


def validate_csrf(user_id: int, token: Optional[str]) -> bool:
	if not token:
		return False
	return _user_csrf_tokens.get(user_id) == token