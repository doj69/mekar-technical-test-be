from pydantic import BaseModel, HttpUrl
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseModel):
    DRIVER: str = "postgresql"
    HOSTNAME: str = "localhost"
    PORT: int = 5432
    PASSWORD: str = "postgres"
    NAME: str = "sqlalchemy-db-test"
    USERNAME: str = "postgres"


class AppConfigSetting(BaseSettings):
    BACKEND_CORS_ORIGINS: list[HttpUrl] = []
    ECHO: bool = False
    SEVERITY_LEVEL: str = "INFO"
    APP_PORT: int = 8000
    DATABASE: DatabaseSettings = DatabaseSettings()

    def get_db_connection(self):
        url = f"{self.DATABASE.DRIVER}://{self.DATABASE.USERNAME}:{self.DATABASE.PASSWORD}@{self.DATABASE.HOSTNAME}:{self.DATABASE.PORT}/{self.DATABASE.NAME}"
        return url


settings = AppConfigSetting()
