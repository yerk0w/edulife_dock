from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.models.registration_request import RegistrationRequest
from app.schemas.user import UserCreate, UserUpdate
from app.security.password import get_password_hash, verify_password

def get_user(db: Session, user_id: int):
    """
    Получение пользователя по ID
    """
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    """
    Получение пользователя по имени пользователя
    """
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str):
    """
    Получение пользователя по email
    """
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    """
    Получение списка пользователей
    """
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    """
    Создание нового пользователя и заявки на регистрацию
    """
    # Проверяем, есть ли пользователь с таким username или email
    if get_user_by_username(db, user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким именем уже существует"
        )
    if get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже существует"
        )
    
    # Создаем хеш пароля
    hashed_password = get_password_hash(user.password)
    
    # Создаем пользователя с ролью и начальным статусом is_active=False
    db_user = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
        role=user.requested_role,  # Устанавливаем запрошенную роль, но админ должен подтвердить
        is_active=False  # Пользователь не активен до одобрения
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Создаем заявку на регистрацию
    db_request = RegistrationRequest(
        user_id=db_user.id,
        requested_role=user.requested_role,
        status="ожидает"
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    """
    Аутентификация пользователя
    """
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def update_user(db: Session, user_id: int, user_update: UserUpdate):
    """
    Обновление данных пользователя
    """
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    # Обновляем только переданные поля
    update_data = user_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def change_user_password(db: Session, user_id: int, old_password: str, new_password: str):
    """
    Изменение пароля пользователя
    """
    db_user = get_user(db, user_id)
    if not db_user:
        return False
    
    # Проверяем старый пароль
    if not verify_password(old_password, db_user.hashed_password):
        return False
    
    # Устанавливаем новый пароль
    db_user.hashed_password = get_password_hash(new_password)
    db.commit()
    return True