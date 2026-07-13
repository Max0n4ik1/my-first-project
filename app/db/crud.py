from typing import Optional
from sqlalchemy.orm import Session
from app.db import models

#CRUD для Category 

def create_category(db: Session, title: str):
    """Создать новую категорию"""
    # Проверяем, существует ли уже категория с таким названием
    existing = db.query(models.Category).filter(models.Category.title == title).first()
    if existing:
        raise ValueError(f"Category '{title}' already exists")
    
    db_category = models.Category(title=title)
    db.add(db_category)
    db.commit()
    return db_category

def get_categories(db: Session):
    """Получить все категории"""
    return db.query(models.Category).all()

def get_category_by_id(db: Session, category_id: int):
    """Получить категорию по ID"""
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def get_category_by_title(db: Session, title: str):
    """Получить категорию по названию"""
    return db.query(models.Category).filter(models.Category.title == title).first()

def update_category(db: Session, category_id: int, new_title: str):
    """Обновить категорию (оптимизированная версия)"""
    # Один запрос: получаем категорию по ID
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        return None
    
    # Если название не меняется — ничего не делаем
    if not new_title or new_title == category.title:
        return category
    
    # Один запрос: проверяем, не занято ли новое название (исключая текущую категорию)
    existing = db.query(models.Category).filter(
        models.Category.title == new_title,
        models.Category.id != category_id
    ).first()
    
    if existing:
        raise ValueError(f"Category '{new_title}' already exists")
    
    # Обновляем
    category.title = new_title
    db.commit()
    return category

def delete_category(db: Session, category_id: int):
    """Удалить категорию"""
    category = get_category_by_id(db, category_id)
    if category:
        db.delete(category)
        db.commit()
    return category

#CRUD для Book

def create_book(db: Session, book_data):
    # Проверяем существование категории
    category = db.query(models.Category).filter(models.Category.id == book_data.category_id).first()
    if not category:
        raise ValueError(f"Category with id {book_data.category_id} not found")
    
    # Создаем книгу
    db_book = models.Book(
        title=book_data.title,
        description=book_data.description,
        price=book_data.price,
        url=book_data.url or "",
        category_id=book_data.category_id
    )
    db.add(db_book)
    db.commit()
    return db_book

def get_books(db: Session, category_id: Optional[int] = None):
    """
    Получить все книги или отфильтровать по категории.
    Если category_id не передан, возвращаются все книги.
    """
    query = db.query(models.Book)
    if category_id is not None:
        query = query.filter(models.Book.category_id == category_id)
    return query.all()

def get_book_by_id(db: Session, book_id: int):
    """Получить книгу по ID"""
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def update_book(db: Session, book_id: int, book_data):
    book = get_book_by_id(db, book_id)
    if not book:
        return None
    
    # Если передан category_id, проверяем существование категории
    if book_data.category_id is not None:
        category = db.query(models.Category).filter(models.Category.id == book_data.category_id).first()
        if not category:
            raise ValueError(f"Category with id {book_data.category_id} not found")
    
    # Обновляем только переданные поля
    update_data = book_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(book, key, value)
    
    db.commit()
    return book

def delete_book(db: Session, book_id: int):
    """Удалить книгу"""
    book = get_book_by_id(db, book_id)
    if book:
        db.delete(book)
        db.commit()
    return book