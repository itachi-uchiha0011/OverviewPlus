# Build frontend
FROM node:20-alpine AS frontend
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json* frontend/pnpm-lock.yaml* ./
RUN npm ci --silent || npm install --silent
COPY frontend .
RUN npm run build

# Backend image
FROM python:3.13-slim AS backend
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY backend/requirements.txt /app/backend/requirements.txt
RUN python -m venv /app/venv && /app/venv/bin/pip install --upgrade pip && /app/venv/bin/pip install -r /app/backend/requirements.txt && /app/venv/bin/pip install gunicorn gevent
COPY backend /app/backend
COPY --from=frontend /app/frontend/dist /app/frontend_dist
ENV FLASK_APP=backend/run.py SOCKETIO_ASYNC_MODE=gevent
EXPOSE 5000
CMD ["/app/venv/bin/gunicorn", "-k", "geventwebsocket.gunicorn.workers.GeventWebSocketWorker", "-w", "1", "-b", "0.0.0.0:5000", "backend.run:app"]