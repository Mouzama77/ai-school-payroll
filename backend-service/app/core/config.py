from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Single source of truth for configuration.
    DATABASE_URL: str = "sqlite:///./school_payroll.db"

    SECRET_KEY: str = "change-me"
    JWT_ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    PROJECT_NAME: str = "School Payroll API"
    DEBUG: bool = False


settings = Settings()


