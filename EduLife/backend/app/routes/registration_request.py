from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.registration_request import RegistrationRequestResponse, RegistrationRequestUpdate
from app.services.registration_request import get_registration_requests, get_registration_request, get_pending_registration_requests, update_registration_request_status
from app.security.jwt import get_admin_user
from app.models.user import User

router = APIRouter(
    prefix="/registration-requests",
    tags=["registration"],
)

@router.get("/", response_model=List[RegistrationRequestResponse])
def read_registration_requests(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """
    Получение всех заявок на регистрацию (только для администраторов)
    """
    return get_registration_requests(db, skip=skip, limit=limit)

@router.get("/pending", response_model=List[RegistrationRequestResponse])
def read_pending_requests(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """
    Получение заявок на регистрацию в статусе "ожидает" (только для администраторов)
    """
    return get_pending_registration_requests(db, skip=skip, limit=limit)

@router.get("/{request_id}", response_model=RegistrationRequestResponse)
def read_registration_request(
    request_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """
    Получение заявки на регистрацию по ID (только для администраторов)
    """
    db_request = get_registration_request(db, request_id=request_id)
    if db_request is None:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    return db_request

@router.patch("/{request_id}", response_model=RegistrationRequestResponse)
def update_request_status(
    request_id: int,
    request_update: RegistrationRequestUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """
    Обновление статуса заявки на регистрацию (только для администраторов)
    """
    db_request = update_registration_request_status(db, request_id=request_id, request_update=request_update)
    if db_request is None:
        raise HTTPException(status_code=404, detail="Заявка не найдена или уже обработана")
    return db_request