from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.database import Base

class RegistrationRequest(Base):
    __tablename__ = "registration_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Enum("ожидает", "одобрено", "отклонено", name="reg_status_enum"), default="ожидает")
    requested_role = Column(Enum("студент", "преподаватель", name="requested_role_enum"), default="студент")
    comment = Column(String(255), nullable=True)  # Комментарий администратора
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    processed_at = Column(DateTime(timezone=True), nullable=True)  # Когда заявка была обработана
    
    # Связь с пользователем
    user = relationship("User", back_populates="registration_request")