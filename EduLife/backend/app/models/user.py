from sqlalchemy import Column, Integer, String, Enum, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    full_name = Column(String(100), nullable=False)
    hashed_password = Column(String(100), nullable=False)
    role = Column(Enum("студент", "преподаватель", "админ", name="role_enum"), default="студент")
    is_active = Column(Boolean, default=False)  # Аккаунт активирован после одобрения заявки
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Связь с документами (один пользователь может создать много документов)
    documents = relationship("Document", back_populates="author")
    
    # Связь с заявками на регистрацию
    registration_request = relationship("RegistrationRequest", back_populates="user", uselist=False)