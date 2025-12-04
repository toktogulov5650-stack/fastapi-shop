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

    # CORS: для продакшена оставляем только нужный порт
    cors_origins: List[str] = [
        "http://localhost:8000",   # один порт для всего
        "http://127.0.0.1:8000",
        "http://localhost:5173",   # на время разработки (если запускаешь отдельно)
        "http://127.0.0.1:5173",
    ]

    # Путь к собранному фронтенду (ВАЖНО: dist, а не frontend)
    static_dir: Path = BASE_DIR / "frontend" / "dist"

    # Путь к assets (js, css, картинки) внутри dist
    images_dir: Path = static_dir / "assets"

    class Config:
        env_file = ".env"  # можно переопределять через .env

# Создаём объект settings для импорта в main.py
settings = Settings()