from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import books, categories
from app.db.db import engine, Base

# Создаём экземпляр приложения FastAPI
app = FastAPI(
    title="Book Catalog API",
    description="API для управления книжным каталогом",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(books.router)
app.include_router(categories.router)


#Health Check 
@app.get("/health", tags=["Health"])
def health_check():
    """
    Проверка работоспособности сервиса.
    Возвращает статус и информацию о сервисе.
    """
    return {
        "status": "ok",
        "service": "Book Catalog API",
        "version": "1.0.0"
    }


#Root endpoint
@app.get("/", tags=["Root"])
def root():
    """
    Корневой эндпоинт.
    Перенаправляет в документацию Swagger.
    """
    return {
        "message": "Welcome to Book Catalog API!",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.on_event("startup")
def startup():
    """Действия при запуске приложения"""
    Base.metadata.create_all(bind=engine)
    print(" Database tables created (if not exists)")
    print(" Server is running at http://127.0.0.1:8000")
    print(" API Documentation: http://127.0.0.1:8000/docs")