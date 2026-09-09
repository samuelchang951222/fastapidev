from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from supabase import create_client

from .frontend import serve_frontend
from .routers import auth, categories, flash_sales, orders, products
from .supabase_config import SUPABASE_KEY, SUPABASE_URL


def create_app() -> FastAPI:
    app = FastAPI(title="鮮採市集 API", version="0.1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health")
    def health() -> dict:
        return {"ok": True}

    app.include_router(auth.router)
    app.include_router(categories.router)
    app.include_router(products.router)
    app.include_router(flash_sales.router)
    app.include_router(orders.router)

    # ── 正式上線：FastAPI 直接 serve 前端 build 好的靜態檔 ──
    build_dir = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"
    if build_dir.exists():
        # 先掛載靜態檔（JS、CSS、圖片等）
        app.mount(
            "/assets",
            StaticFiles(directory=str(build_dir / "assets")),
            name="assets",
        )
        # SPA fallback — 所有非 API 路由都導到 index.html
        @app.get("/{full_path:path}")
        async def spa_fallback(full_path: str):
            return serve_frontend(build_dir, full_path)

        print(f"✅ 前端靜態檔已掛載 ({build_dir})")

    return app


app = create_app()

# ── 啟動時補上訪客使用者（讓訂單外鍵不炸） ──
try:
    sb = create_client(SUPABASE_URL, SUPABASE_KEY)
    # 直接 upsert，id=0 已存在就不動
    sb.table("users").upsert(
        {"id": 0, "name": "訪客", "email": "guest@local", "hashed_password": "no-auth"},
        on_conflict="id"
    ).execute()
except Exception:
    pass

