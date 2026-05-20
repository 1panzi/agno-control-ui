from __future__ import annotations
from pathlib import Path
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict

LOG_DIR = Path(__file__).parent.parent / "logs"

_ENV_FILE = Path(__file__).parent.parent / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(_ENV_FILE),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # App
    app_name: str = "agno-platform"
    app_env: Literal["development", "production"] = "development"
    LOGGER_LEVEL: str = "INFO"

    # Database
    database_url: str

    # Vector DB（空 → 复用 database_url）
    vector_db_url: str = ""

    # Embedder
    embedder_base_url: str = ""
    embedder_api_key: str = ""
    embedder_model: str = "BAAI/bge-large-zh-v1.5"
    embedder_dimensions: int = 1024

    # API
    api_cors_origins: list[str] = ["*"]

    # Skill market
    skill_market_url: str = "https://api.github.com/repos/agno-agi/agno/contents/cookbook/skills"

    @property
    def effective_vector_db_url(self) -> str:
        return self.vector_db_url or self.database_url


settings = Settings()
