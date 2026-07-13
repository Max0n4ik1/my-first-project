import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.db import SessionLocal, engine, Base
from app.db import models
from app.db.crud import create_category, create_book, get_category_by_title, get_categories, get_books
from app.schemas import BookCreate

Base.metadata.create_all(bind=engine)

def init_database():
    db = SessionLocal()
    
    try:
        # Создаём категории
        categories_data = [
            {"title": "Фантастика"},
            {"title": "Детективы"},
            {"title": "Научная литература"},
            {"title": "Классика"}
        ]
        
        created_categories = []
        for cat_data in categories_data:
            existing = get_category_by_title(db, cat_data["title"])
            if not existing:
                category = create_category(db, cat_data["title"])
                created_categories.append(category)
                print(f"✅ Создана категория: {category.title}")
            else:
                print(f"⚠️ Категория '{cat_data['title']}' уже существует")
                created_categories.append(existing)
        
        # Создаём книги
        books_data = [
            {"title": "Дюна", "description": "Эпическая сага о пустынной планете", "price": 899.0, "category_title": "Фантастика", "url": "https://example.com/duna"},
            {"title": "Нейромант", "description": "Классика киберпанка", "price": 749.0, "category_title": "Фантастика", "url": "https://example.com/neuromant"},
            {"title": "Автостопом по галактике", "description": "Юмористическая фантастика", "price": 699.0, "category_title": "Фантастика", "url": "https://example.com/hitchhiker"},
            {"title": "Убийство в Восточном экспрессе", "description": "Классический детектив Агаты Кристи", "price": 599.0, "category_title": "Детективы", "url": "https://example.com/orient_express"},
            {"title": "Собака Баскервилей", "description": "Приключения Шерлока Холмса", "price": 649.0, "category_title": "Детективы", "url": "https://example.com/baskerville"},
            {"title": "Девушка с татуировкой дракона", "description": "Скандинавский детектив", "price": 799.0, "category_title": "Детективы", "url": "https://example.com/dragon_tattoo"},
            {"title": "Краткая история времени", "description": "Стивен Хокинг о космологии", "price": 999.0, "category_title": "Научная литература", "url": "https://example.com/brief_history"},
            {"title": "Эгоистичный ген", "description": "Ричард Докинз об эволюции", "price": 879.0, "category_title": "Научная литература", "url": "https://example.com/selfish_gene"},
            {"title": "Война и мир", "description": "Эпопея Льва Толстого", "price": 1299.0, "category_title": "Классика", "url": "https://example.com/war_and_peace"},
            {"title": "Преступление и наказание", "description": "Роман Фёдора Достоевского", "price": 899.0, "category_title": "Классика", "url": "https://example.com/crime_and_punishment"},
        ]
        
        for book_data in books_data:
            category = get_category_by_title(db, book_data["category_title"])
            if category:
                existing_books = get_books(db)
                exists = any(b.title == book_data["title"] for b in existing_books)
                if not exists:
                    # Создаём объект BookCreate
                    book_create = BookCreate(
                        title=book_data["title"],
                        description=book_data["description"],
                        price=book_data["price"],
                        category_id=category.id,
                        url=book_data["url"]
                    )
                    book = create_book(db, book_create)
                    print(f"📚 Создана книга: {book.title} (категория: {category.title})")
                else:
                    print(f"⚠️ Книга '{book_data['title']}' уже существует")
            else:
                print(f"❌ Категория '{book_data['category_title']}' не найдена!")
        
        print("\n🎉 База данных успешно инициализирована!")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()