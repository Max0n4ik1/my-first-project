import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.db import SessionLocal
from app.db.crud import get_categories, get_books

def main():
    """Выводим данные из базы данных"""
    db = SessionLocal()
    
    try:
        print("\n" + "="*60)
        print("📚 КНИЖНЫЙ КАТАЛОГ")
        print("="*60)
        
        # Получаем все категории
        categories = get_categories(db)
        print(f"\n📂 Всего категорий: {len(categories)}")
        
        for category in categories:
            print(f"\n📖 {category.title.upper()}:")
            
            # Получаем книги для этой категории
            books = get_books(db)
            category_books = [b for b in books if b.category_id == category.id]
            
            if category_books:
                for book in category_books:
                    print(f"   • {book.title} — {book.price} руб.")
                    if book.description:
                        print(f"     {book.description[:60]}...")
            else:
                print("   (нет книг в этой категории)")
        
        print("\n" + "="*60)
        print(f"📊 Итого: {len(categories)} категорий, {len(get_books(db))} книг")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main()