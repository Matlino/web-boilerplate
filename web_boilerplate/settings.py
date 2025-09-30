from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)

    # Default to local Postgres via peer auth (macOS/Linux):
    # Example: postgresql+asyncpg://localhost/app_db
    database_url: str = Field(
        default="postgresql+asyncpg://localhost/app_db",
        alias="DATABASE_URL",
    )


settings = Settings()


