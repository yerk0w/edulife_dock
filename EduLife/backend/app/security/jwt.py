from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.schemas.token import TokenData
from app.db.database import get_db
from app.models.user import User
import secrets

# Настройки JWT
SECRET_KEY = secrets.token_hex(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2 схема для получения токена из заголовка Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Создание JWT-токена
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Получение текущего пользователя по токену
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Некорректные учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """
    Проверка, что пользователь активирован
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Аккаунт не активирован")
    return current_user

# Зависимость для проверки роли
def get_user_by_role(required_role: str):
    """
    Фабрика зависимостей для проверки роли пользователя
    """
    async def _get_user_by_role(current_user: User = Depends(get_current_active_user)):
        if current_user.role != required_role and current_user.role != "админ":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Для выполнения операции требуется роль {required_role}",
            )
        return current_user
    return _get_user_by_role

# Зависимости для различных ролей
get_admin_user = get_user_by_role("админ")
get_teacher_user = get_user_by_role("преподаватель")
get_student_user = get_user_by_role("студент")