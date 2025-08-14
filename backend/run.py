from app import create_app
from app.extensions import socketio
from flask import send_from_directory
import os

app = create_app()

FRONTEND_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend_dist"))

@app.get("/")
def index():
	index_path = os.path.join(FRONTEND_ROOT, "index.html")
	if os.path.exists(index_path):
		return send_from_directory(FRONTEND_ROOT, "index.html")
	return {"app": app.config.get("APP_NAME", "Overview+")}

@app.get("/assets/<path:filename>")
def assets(filename: str):
	return send_from_directory(os.path.join(FRONTEND_ROOT, "assets"), filename)

@app.get("/service-worker.js")
def sw():
	return send_from_directory(FRONTEND_ROOT, "service-worker.js")

@app.get("/favicon.ico")
def favicon():
	return send_from_directory(FRONTEND_ROOT, "favicon.ico")

if __name__ == "__main__":
	socketio.run(app, host="0.0.0.0", port=5000, debug=app.config.get("DEBUG", True))