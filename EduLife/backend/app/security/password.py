from passlib.context import CryptContext

# Создаем контекст для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    """
    Проверка пароля по хешу
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """
    Получение хеша пароля
    """
    return pwd_context.hash(password)