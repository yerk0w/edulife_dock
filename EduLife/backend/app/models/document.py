from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(
        Enum("ожидает", "одобрено", "отклонено", name="status_enum"),
        default="ожидает",
    )
    
    # Связь с пользователем-автором
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    author = relationship("User", back_populates="documents")
    
    # Тип шаблона (если документ создан на основе шаблона)
    template_type = Column(String(50), nullable=True)