from __future__ import annotations

from typing import List

from pydantic import field_validator, FieldValidationInfo
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Primary configuration
    DATABASE_URL: str = "sqlite:///./app.db"
    SECRET_KEY: str = "change-this-secret-for-production"

    # JWT settings
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24 * 7  # 7 days
    ALGORITHM: str = "HS256"

    # CORS / frontend
    CORS_ORIGINS: str = "http://localhost:5173"

    # Feature flags
    ENABLE_DB_SEED: bool = True
    ENV: str = "development"  # e.g. development / production

    # ECPay settings
    ECPAY_MERCHANT_ID: str = ""
    ECPAY_HASH_KEY: str = ""
    ECPAY_HASH_IV: str = ""
    ECPAY_ENV: str = "test"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
