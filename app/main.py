from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from .config import settings
from .database import init_db
from .routes import products_router, categories_router, cart_router

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


# -------------------
# Статические файлы (assets)
# -------------------
ASSETS_DIR = Path(settings.static_dir) / "assets"  # например frontend/assets
if ASSETS_DIR.exists():
    app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")
else:
    print(f"Warning: папка {ASSETS_DIR} не найдена")

# -------------------
# Vue SPA: отдаём index.html для всех маршрутов, кроме /api и /assets
# -------------------
INDEX_FILE = Path(settings.static_dir) / "index.html"


@app.get("/{full_path:path}")
def serve_vue_app(full_path: str):
    # Игнорируем маршруты API и assets
    if full_path.startswith("api") or full_path.startswith("assets"):
        return {"error": "Not found"}

    if INDEX_FILE.exists():
        return FileResponse(INDEX_FILE)
    return {"error": "index.html not found"}


# -------------------
# Root API
# -------------------
@app.get("/api")
def root():
    return {
        "message": "Welcome to fastapi shop API",
        "docs": "/api/docs",
    }


# -------------------
# Health check
# -------------------
@app.get("/health")
def health_check():
    return {"status": "healthy"}

















