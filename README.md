# 鮮採市集

Vue 3 + FastAPI 線上蔬果市集。

## 開發

**後端**（Python 3.10+）

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

> macOS 系統 Python 是 3.9，用 `brew install python@3.12` 裝新版。

**前端**（Node 18+）

```bash
cd frontend
npm install
npm run dev
```

後端 `localhost:8000`，前端 `localhost:5173`（開發模式會 proxy `/api` 到後端）。

## 正式上線

```bash
cd frontend && npm run build
cd .. && uvicorn main:app --host 0.0.0.0 --port 8000
```

合併成單一 port。

## 專案結構

```
backend/app/
├── main.py             入口 + SPA fallback
├── schemas.py          Pydantic models
├── supabase_config.py  Supabase 連線
└── routers/            API 路由（auth, products, categories, orders...）

frontend/src/
├── main.js             啟動
├── router/             路由
├── stores/             Pinia（auth, cart, catalog, ui, toast）
├── components/         元件（HeaderNav, CartDrawer, ProductCard...）
└── views/              頁面（Home, Shop, Product, Checkout, Login...）
```

## 問題

| 問題 | 解法 |
|------|------|
| Python < 3.10 | `brew install python@3.12` (Mac) / `apt install python3.11` (Linux) |
| `pip install` 失敗 | `pip install --upgrade pip` |
| Supabase 連不上 | 改 `backend/app/supabase_config.py` 的 URL 跟 key |
