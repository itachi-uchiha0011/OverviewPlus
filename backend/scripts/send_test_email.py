import sys
from app import create_app
from app.utils.emailer import send_email


def main():
    if len(sys.argv) < 2:
        print("Usage: python send_test_email.py <to_email>")
        sys.exit(1)
    to_email = sys.argv[1]
    app = create_app()
    with app.app_context():
        ok = send_email(to_email, "Overview+ Test Email", "<p>Hello from Overview+.</p>")
        print("OK" if ok else "FAILED")


if __name__ == "__main__":
    main()