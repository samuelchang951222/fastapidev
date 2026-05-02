"""
鮮採市集 — 整合入口

開發模式：
  uvicorn backend.app.main:app --reload --port 8000
  (另一個 terminal) cd frontend && npm run dev

正式上線（前端已 build）：
  uvicorn main:app --host 0.0.0.0 --port 8000
"""

from backend.app.main import app
