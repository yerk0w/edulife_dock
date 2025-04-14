from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.user import UserResponse, UserUpdate, UserChangePassword
from app.services.user import get_users, get_user, update_user, change_user_password
from app.security.jwt import get_current_active_user, get_admin_user
from app.models.user import User

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
    Получение данных текущего пользователя
    """
    return current_user

@router.get("/", response_model=List[UserResponse])
def read_users(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """
    Получение списка всех пользователей (только для администраторов)
    """
    users = get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=UserResponse)
def read_user(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """
    Получение пользователя по ID (только для администраторов)
    """
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return db_user

@router.put("/me", response_model=UserResponse)
def update_user_me(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Обновление данных текущего пользователя
    """
    updated_user = update_user(db, user_id=current_user.id, user_update=user_update)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return updated_user

@router.post("/me/change-password", status_code=status.HTTP_200_OK)
def change_password(
    password_data: UserChangePassword,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Изменение пароля текущего пользователя
    """
    success = change_user_password(
        db, 
        user_id=current_user.id, 
        old_password=password_data.old_password, 
        new_password=password_data.new_password
    )
    if not success:
        raise HTTPException(status_code=400, detail="Неверный текущий пароль")
    return {"message": "Пароль успешно изменен"}