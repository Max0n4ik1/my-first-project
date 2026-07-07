from sqlalchemy.orm import Session
from app.db import models

#CRUD для Category 

def create_category(db: Session, title: str):
    """Создать новую категорию"""
    db_category = models.Category(title=title)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
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
    """Обновить категорию"""
    category = get_category_by_id(db, category_id)
    if category:
        category.title = new_title
        db.commit()
        db.refresh(category)
    return category

def delete_category(db: Session, category_id: int):
    """Удалить категорию"""
    category = get_category_by_id(db, category_id)
    if category:
        db.delete(category)
        db.commit()
    return category

#CRUD для Book

def create_book(db: Session, title: str, description: str, price: float, category_id: int, url: str = ""):
    """Создать новую книгу"""
    db_book = models.Book(
        title=title,
        description=description,
        price=price,
        url=url,
        category_id=category_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_books(db: Session):
    """Получить все книги"""
    return db.query(models.Book).all()

def get_books_by_category(db: Session, category_id: int):
    """Получить книги по категории"""
    return db.query(models.Book).filter(models.Book.category_id == category_id).all()

def get_book_by_id(db: Session, book_id: int):
    """Получить книгу по ID"""
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def update_book(db: Session, book_id: int, title: str = None, description: str = None, price: float = None, url: str = None):
    """Обновить книгу"""
    book = get_book_by_id(db, book_id)
    if book:
        if title is not None:
            book.title = title
        if description is not None:
            book.description = description
        if price is not None:
            book.price = price
        if url is not None:
            book.url = url
        db.commit()
        db.refresh(book)
    return book

def delete_book(db: Session, book_id: int):
    """Удалить книгу"""
    book = get_book_by_id(db, book_id)
    if book:
        db.delete(book)
        db.commit()
    return book