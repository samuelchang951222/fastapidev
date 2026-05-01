"""
應用程式設定
"""
from __future__ import annotations
from typing import List
from pydantic import field_validator, FieldValidationInfo
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres.igzekhhebnvuamisualh:WL82YvgaAFsnVqnT@aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres"
    SECRET_KEY: str = "change-this-secret-for-production"
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24 * 7
    ALGORITHM: str = "HS256"
    CORS_ORIGINS: str = "http://localhost:5173"
    ENABLE_DB_SEED: bool = True
    ENV: str = "development"
    ECPAY_MERCHANT_ID: str = ""
    ECPAY_HASH_KEY: str = ""
    ECPAY_HASH_IV: str = ""
    ECPAY_ENV: str = "test"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
