from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import books, categories
from app.db.db import engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created (if not exists)")
    print("🚀 Server is running at http://127.0.0.1:8000")
    print("📚 API Documentation: http://127.0.0.1:8000/docs")
    yield
    # Действия при остановке
    print(" Server is shutting down...")


app = FastAPI(
    title="Book Catalog API",
    description="API для управления книжным каталогом",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(books.router)
app.include_router(categories.router)


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "service": "Book Catalog API",
        "version": "1.0.0"
    }


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Welcome to Book Catalog API!",
        "docs": "/docs",
        "redoc": "/redoc"
    }