from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel

class RegistrationRequestBase(BaseModel):
    requested_role: Literal["студент", "преподаватель"] = "студент"

class RegistrationRequestCreate(RegistrationRequestBase):
    user_id: int

class RegistrationRequestUpdate(BaseModel):
    status: Literal["одобрено", "отклонено"]
    comment: Optional[str] = None

class RegistrationRequestResponse(RegistrationRequestBase):
    id: int
    user_id: int
    status: str
    comment: Optional[str] = None
    created_at: datetime
    processed_at: Optional[datetime] = None

    class Config:
        from_attributes = True
