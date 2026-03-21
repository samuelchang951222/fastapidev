from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers (modular endpoints)
from .routers import auth, categories, products, orders, flash_sales

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
    app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
    app.include_router(categories.router, prefix="/api/categories", tags=["categories"])
    app.include_router(products.router, prefix="/api/products", tags=["products"])
    app.include_router(orders.router, prefix="/api/orders", tags=["orders"])
    app.include_router(flash_sales.router, prefix="/api/flash-sales", tags=["flash-sales"])

    return app

app = create_app()