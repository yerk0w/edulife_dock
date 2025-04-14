from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.user import User
from app.models.registration_request import RegistrationRequest
from app.security.password import get_password_hash

def create_admin():
    db = SessionLocal()
    try:
        # Проверяем, есть ли уже админ
        admin = db.query(User).filter(User.role == "админ").first()
        if admin:
            print("Администратор уже существует!")
            return
        
        # Создаем администратора
        admin = User(
            username="admin",
            email="admin@example.com",
            full_name="Администратор Системы",
            hashed_password=get_password_hash("admin123"),
            role="админ",
            is_active=True
        )
        db.add(admin)
        db.commit()
        
        # Создаем заявку (для поддержания целостности данных)
        req = RegistrationRequest(
            user_id=admin.id,
            status="одобрено",
            requested_role="админ"
        )
        db.add(req)
        db.commit()
        
        print("Администратор успешно создан!")
        print("Логин: admin")
        print("Пароль: admin123")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()