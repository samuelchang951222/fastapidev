from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import categories, flash_sales, products


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

    app.include_router(categories.router)
    app.include_router(products.router)
    app.include_router(flash_sales.router)

    return app


app = create_app()

