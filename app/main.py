from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from .config import settings
from .database import init_db
from .routes import products_router, categories_router, cart_router
from .seed_data import seed_database  # ← Добавили импорт

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    docs_url='/api/docs',
    redoc_url='/api/redoc'
)

# -------------------
# CORS
# -------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------
# API роутеры
# -------------------
app.include_router(products_router)
app.include_router(categories_router)
app.include_router(cart_router)


# -------------------
# Инициализация базы
# -------------------
@app.on_event('startup')
def on_startup():
    init_db()
    # Запускаем заполнение базы тестовыми данными
    try:
        seed_database()
        print("✅ Seed data executed successfully")
    except Exception as e:
        print(f"⚠️ Seed data warning: {e}")
        # Не падаем если данные уже есть


# -------------------
# Root API - ДОЛЖЕН БЫТЬ ДО catch-all!
# -------------------
@app.get("/api")
def root():
    return {
        "message": "Welcome to fastapi shop API",
        "docs": "/api/docs",
    }


# -------------------
# Health check - ДОЛЖЕН БЫТЬ ДО catch-all!
# -------------------
@app.get("/health")
def health_check():
    return {"status": "healthy"}


# -------------------
# Статические файлы (assets)
# -------------------
ASSETS_DIR = Path(settings.static_dir) / "assets"
if ASSETS_DIR.exists():
    app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")
else:
    print(f"Warning: папка {ASSETS_DIR} не найдена")


# -------------------
# Debug endpoint для проверки API
# -------------------
@app.get("/api/test")
def test_api():
    return {
        "message": "Test API работает!",
        "timestamp": "2024-01-15T12:00:00",
        "routes": ["/api", "/api/categories", "/api/cart", "/api/docs"]
    }


# -------------------
# Debug endpoint для проверки всех роутов
# -------------------
@app.get("/api/debug/routes")
def debug_routes():
    routes = []
    for route in app.routes:
        route_info = {
            "path": route.path,
            "name": route.name,
        }
        if hasattr(route, 'methods'):
            route_info["methods"] = list(route.methods)
        routes.append(route_info)

    return {
        "total_routes": len(routes),
        "routes": routes,
        "static_dir": str(settings.static_dir),
        "index_file_exists": Path(settings.static_dir / "index.html").exists()
    }


# -------------------
# Vue SPA: отдаём index.html для всех остальных маршрутов
# -------------------
INDEX_FILE = Path(settings.static_dir) / "index.html"


@app.get("/{full_path:path}")
def serve_vue_app(full_path: str):
    """
    Catch-all роут для фронтенда.
    ВАЖНО: Этот роут должен быть ПОСЛЕДНИМ в файле!
    """
    # Если запрос начинается с api - это должно было обработаться выше
    # Но на всякий случай проверяем и возвращаем 404
    if full_path.startswith("api"):
        raise HTTPException(status_code=404, detail="API endpoint not found")

    # Игнорируем маршруты к assets
    if full_path.startswith("assets"):
        raise HTTPException(status_code=404, detail="Asset not found")

    if INDEX_FILE.exists():
        return FileResponse(INDEX_FILE)

    raise HTTPException(status_code=404, detail="Frontend not found")