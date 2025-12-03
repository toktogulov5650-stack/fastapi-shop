from pathlib import Path
from pydantic_settings import BaseSettings
from typing import List

# Корень проекта fastapi-shop
BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    app_name: str = "FastAPI Shop"
    debug: bool = True

    # URL базы данных
    database_url: str = "sqlite:///./shop.db"

    # CORS: разрешённые адреса фронтенда
    cors_origins: List[str] = [
        "http://localhost:5173",  # Vue dev server
        "http://127.0.0.1:5173",
        "http://localhost:3000",  # альтернативный порт
        "http://127.0.0.1:3000",
    ]

    # Путь к фронтенду без dist
    static_dir: Path = BASE_DIR / "frontend"

    # Путь к assets (js, css, картинки)
    images_dir: Path = static_dir / "assets"

    class Config:
        env_file = ".env"  # можно переопределять через .env

# Создаём объект settings для импорта в main.py
settings = Settings()
