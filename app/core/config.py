import os


class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./prosenos.db")
    APP_TITLE: str = os.getenv("APP_TITLE", "Prosenos")


settings = Settings()
