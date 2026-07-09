from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.db.db import get_db
from app.db import crud
from app.schemas import BookCreate, BookUpdate, BookResponse

# Создаём роутер для книг с префиксом /books
router = APIRouter(prefix="/books", tags=["Books"])


# ========== GET /books (с фильтрацией по категории) ==========
@router.get("/", response_model=list[BookResponse])
def get_all_books(
    category_id: Optional[int] = Query(None, description="ID категории для фильтрации"),
    db: Session = Depends(get_db)
):
    """
    Получить список всех книг.
    Можно отфильтровать по категории, передав category_id.
    """
    if category_id:
        # Проверяем, существует ли такая категория
        category = crud.get_category_by_id(db, category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Категория с ID {category_id} не найдена"
            )
        books = crud.get_books_by_category(db, category_id)
    else:
        books = crud.get_books(db)
    
    return books


# ========== GET /books/{book_id} ==========
@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """Получить книгу по ID"""
    book = crud.get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Книга с ID {book_id} не найдена"
        )
    return book


# ========== POST /books ==========
@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book_data: BookCreate, db: Session = Depends(get_db)):
    """Создать новую книгу"""
    # Проверяем, существует ли категория
    category = crud.get_category_by_id(db, book_data.category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Категория с ID {book_data.category_id} не найдена"
        )
    
    # Проверяем, нет ли книги с таким названием (опционально)
    existing_books = crud.get_books(db)
    if any(b.title == book_data.title for b in existing_books):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Книга '{book_data.title}' уже существует"
        )
    
    return crud.create_book(
        db,
        title=book_data.title,
        description=book_data.description,
        price=book_data.price,
        category_id=book_data.category_id,
        url=book_data.url or ""  # Если URL не передан, ставим пустую строку
    )


# ========== PUT /books/{book_id} ==========
@router.put("/{book_id}", response_model=BookResponse)
def update_book(
    book_id: int,
    book_data: BookUpdate,
    db: Session = Depends(get_db)
):
    """Обновить книгу"""
    # Проверяем, существует ли книга
    existing_book = crud.get_book_by_id(db, book_id)
    if not existing_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Книга с ID {book_id} не найдена"
        )
    
    # Если передан новый category_id, проверяем, существует ли категория
    if book_data.category_id:
        category = crud.get_category_by_id(db, book_data.category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Категория с ID {book_data.category_id} не найдена"
            )
    
    # Обновляем книгу (передаём только те поля, которые были переданы)
    return crud.update_book(
        db,
        book_id,
        title=book_data.title,
        description=book_data.description,
        price=book_data.price,
        url=book_data.url
    )


# ========== DELETE /books/{book_id} ==========
@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Удалить книгу"""
    book = crud.get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Книга с ID {book_id} не найдена"
        )
    crud.delete_book(db, book_id)
    return None