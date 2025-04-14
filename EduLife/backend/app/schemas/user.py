from datetime import datetime
from typing import Optional, List, Literal
from pydantic import BaseModel, EmailStr, Field, constr

class UserBase(BaseModel):
    username: constr(min_length=3, max_length=50)
    email: EmailStr
    full_name: constr(min_length=3, max_length=100)
    role: Literal["студент", "преподаватель", "админ"] = "студент"

class UserCreate(UserBase):
    password: constr(min_length=8)
    requested_role: Literal["студент", "преподаватель"] = "студент"

class UserLogin(BaseModel):
    username: str
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[constr(min_length=3, max_length=100)] = None
    email: Optional[EmailStr] = None

class UserChangePassword(BaseModel):
    old_password: str
    new_password: constr(min_length=8)

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True