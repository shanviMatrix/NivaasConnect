from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict
from psycopg.conninfo import make_conninfo


class Settings(BaseSettings):
    app_name: str = "NivaasConnect API"
    app_env: str = "development"
    api_v1_prefix: str = "/api/v1"

    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "nivaasconnect_db"
    db_user: str = "nivaasconnect_user"
    db_password: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="NIVAAS_",
        extra="ignore",
    )

    @property
    def database_conninfo(self) -> str:
        return make_conninfo(
            host=self.db_host,
            port=self.db_port,
            dbname=self.db_name,
            user=self.db_user,
            password=self.db_password,
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
