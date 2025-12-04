from pathlib import Path
from pydantic_settings import BaseSettings
from typing import List
import os

# Корень проекта fastapi-shop
BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    app_name: str = "FastAPI Shop"
    debug: bool = True

    # URL базы данных
    database_url: str = "sqlite:///./shop.db"

    # CORS: динамически добавляем домен Render
    cors_origins: List[str] = [
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    # Путь к собранному фронтенду
    static_dir: Path = BASE_DIR / "frontend" / "dist"

    # Путь к assets
    images_dir: Path = static_dir / "assets"

    class Config:
        env_file = ".env"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Добавляем Render URL в CORS если он есть
        render_url = os.getenv("RENDER_EXTERNAL_URL")
        if render_url and render_url not in self.cors_origins:
            self.cors_origins.append(render_url)


# Создаём объект settings
settings = Settings()

