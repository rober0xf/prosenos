import os


class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./prosenos.db")
    APP_TITLE: str = os.getenv("APP_TITLE", "Prosenos")
    FUTBOL_SCRAPER_URL: str = os.getenv("SCRAPER_BASE_URL", "http://localhost:8001")
    HOST: str = os.getenv("APP_HOST", "127.0.0.1")
    PORT: int = int(os.getenv("APP_PORT", "8000"))
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = ENVIRONMENT == "environment"


settings = Settings()
