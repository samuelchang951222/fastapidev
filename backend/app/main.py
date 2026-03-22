from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import ecpay

# Import routers (modular endpoints)
from .routers import auth, categories, products, orders, flash_sales, ecpay

# Import database and seed logic
from .db import engine, SessionLocal
from .models import Base
from .services.seed_db import seed_if_empty
from .settings import settings

def create_app() -> FastAPI: 
    app = FastAPI(title="E-Commerce API", version="1.0.0")

    # CORS setup - allow frontend to access API
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Startup event: create tables and seed DB 
    @app.on_event("startup")
    def on_startup():
        Base.metadata.create_all(bind=engine)
        if settings.ENABLE_DB_SEED:
            with SessionLocal() as db:
                seed_if_empty(db)

    # Health check endpoint 
    @app.get("/health")
    def health():
        return {"ok": True}

    # Root endpoint 
    @app.get("/")
    def root():
        return {"message": "hello world"}

    # Register routers 
    app.include_router(auth.router, tags=["auth"])
    app.include_router(categories.router, tags=["categories"])
    app.include_router(products.router, tags=["products"])
    app.include_router(orders.router, tags=["orders"])
    app.include_router(flash_sales.router, tags=["flash-sales"])
    # app.include_router(ecpay.router, prefix="/api/ecpay", tags=["ecpay"])
    return app

app = create_app()