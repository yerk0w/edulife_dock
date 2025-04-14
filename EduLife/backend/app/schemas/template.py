from datetime import datetime
from typing import Optional
from pydantic import BaseModel, constr

class TemplateBase(BaseModel):
    name: constr(min_length=1, max_length=100)
    description: Optional[str] = None
    available_for_students: bool = True
    available_for_teachers: bool = True

class TemplateCreate(TemplateBase):
    pass

class TemplateUpdate(BaseModel):
    name: Optional[constr(min_length=1, max_length=100)] = None
    description: Optional[str] = None
    available_for_students: Optional[bool] = None
    available_for_teachers: Optional[bool] = None

class TemplateResponse(TemplateBase):
    id: int
    file_path: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True