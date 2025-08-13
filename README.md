Overview+ (Full-Stack)

Quickstart

Backend
- cd backend
- python -m venv .venv && source .venv/bin/activate
- pip install -r requirements.txt
- cp ../.env.example ../.env (edit values)
- flask db migrate -m "initial"
- flask db upgrade
- python run.py

Frontend
- cd frontend
- npm install
- npm run dev

Open http://localhost:5173 and sign up.

Tech
- Flask, SQLAlchemy, JWT, Socket.IO
- React, Vite, TailwindCSS
- MySQL/PostgreSQL (configurable via DATABASE_URL)