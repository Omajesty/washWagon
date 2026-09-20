from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str | None = None
    SECRET_KEY: str | None = None
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 60
    BANK_API_KEY = "washwagon"


    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()