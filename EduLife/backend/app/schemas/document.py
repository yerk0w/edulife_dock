from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field, constr

class DocumentBase(BaseModel):
    title: constr(min_length=1, max_length=100)
    content: constr(min_length=1)
    template_type: Optional[str] = None

class DocumentCreate(DocumentBase):
    pass

class DocumentUpdate(BaseModel):
    status: Literal["ожидает", "одобрено", "отклонено"]

class DocumentResponse(DocumentBase):
    id: int
    created_at: datetime
    status: str
    author_id: int
    author_name: str  # Добавляем имя автора для удобства

    class Config:
        from_attributes = True