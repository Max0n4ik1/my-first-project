from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.db import get_db
from app.db import crud
from app.schemas import CategoryCreate, CategoryUpdate, CategoryResponse

# Создаём роутер для категорий с префиксом /categories
router = APIRouter(prefix="/categories", tags=["Categories"])


#GET /categories 
@router.get("/", response_model=list[CategoryResponse])
def get_all_categories(db: Session = Depends(get_db)):
    """Получить список всех категорий"""
    categories = crud.get_categories(db)
    return categories


#GET /categories/{category_id} 
@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """Получить категорию по ID"""
    category = crud.get_category_by_id(db, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Категория с ID {category_id} не найдена"
        )
    return category


# POST /categories 
@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category_data: CategoryCreate, db: Session = Depends(get_db)):
    """Создать новую категорию"""
    # Проверяем, существует ли уже категория с таким названием
    existing = crud.get_category_by_title(db, category_data.title)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Категория '{category_data.title}' уже существует"
        )
    return crud.create_category(db, category_data.title)


#PUT /categories/{category_id}
@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db)
):
    """Обновить категорию"""
    # Проверяем, существует ли категория
    existing = crud.get_category_by_id(db, category_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Категория с ID {category_id} не найдена"
        )
    
    # Если передан новый заголовок, проверяем, не занят ли он
    if category_data.title:
        title_exists = crud.get_category_by_title(db, category_data.title)
        if title_exists and title_exists.id != category_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Категория '{category_data.title}' уже существует"
            )
    
    return crud.update_category(db, category_id, category_data.title)


# DELETE /categories/{category_id} 
@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """Удалить категорию"""
    category = crud.get_category_by_id(db, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Категория с ID {category_id} не найдена"
        )
    crud.delete_category(db, category_id)
    return None