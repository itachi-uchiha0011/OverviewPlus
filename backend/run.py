from app import create_app
from app.extensions import socketio
from flask import send_from_directory
import os

app = create_app()

@app.get("/")
def index():
	root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend_dist"))
	index_path = os.path.join(root, "index.html")
	if os.path.exists(index_path):
		return send_from_directory(root, "index.html")
	return {"app": app.config.get("APP_NAME", "Overview+")}

if __name__ == "__main__":
	socketio.run(app, host="0.0.0.0", port=5000, debug=app.config.get("DEBUG", True))