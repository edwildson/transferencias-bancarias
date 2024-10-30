import logging
from typing import Optional
from src.schemas import settings_schemas
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_nested_delimiter="__", extra="allow",
    )

    SERVER: settings_schemas.ServerSettings = settings_schemas.ServerSettings()

    DEVELOP: bool = True  # `True` -> gera documentação completa em `/redoc`

    LOGGING_LEVEL: Optional[int] = logging.INFO
    LOGGING_FILE: Optional[bool] = False

    DEFAULT_API_SERVICE_TIMEOUT: int = 30

    DATABASE_URL: str = "postgresql+asyncpg://backend:backend@db_postgres/backend"
    JWT_SECRET: str = "ddb2b757275f9220dbb389cf412dd6c5"

    KAFKA: settings_schemas.KAFKA = settings_schemas.KAFKA()
