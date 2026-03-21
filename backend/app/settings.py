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
    CORS_ORIGINS: List[str] = ["http://localhost:5173"]

    # Feature flags
    ENABLE_DB_SEED: bool = True
    ENV: str = "development"  # e.g. development / production

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @field_validator("SECRET_KEY")
    def ensure_secret_key(cls, v: str, info: FieldValidationInfo) -> str:
        if not v or v.strip() == "":
            raise ValueError("SECRET_KEY must be set")

        env = info.data.get("ENV") or ""
        # Warn if using the placeholder secret in a non-production environment.
        if v == "change-this-secret-for-production" and env != "production":
            # keep default for local dev but remind user to change it
            print(
                "WARNING: Using default SECRET_KEY. Set SECRET_KEY env var for production security."
            )
        return v


settings = Settings()
