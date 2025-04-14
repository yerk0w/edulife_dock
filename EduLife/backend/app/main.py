import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from pathlib import Path

from app.db.database import engine
from app.models import document, user, registration_request, template
from app.routes import router

# Создаем директории для статических файлов и шаблонов
STATIC_DIR = Path("app/static")
TEMPLATES_DIR = Path("app/static/templates")
os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(TEMPLATES_DIR, exist_ok=True)

# Создаем таблицы в БД
document.Base.metadata.create_all(bind=engine)
user.Base.metadata.create_all(bind=engine)
registration_request.Base.metadata.create_all(bind=engine)
template.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Document Service API",
    description="API для микросервиса документооборота с поддержкой ролей",
    version="0.2.0",
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем статические файлы
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Подключаем роуты
app.include_router(router)

@app.get("/", response_class=HTMLResponse)
def read_root():
    """
    Перенаправление на статическую страницу
    """
    return RedirectResponse(url="/static/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)