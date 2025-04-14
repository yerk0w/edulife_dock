from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.registration_request import RegistrationRequest
from app.models.user import User
from app.schemas.registration_request import RegistrationRequestUpdate

def get_registration_requests(db: Session, skip: int = 0, limit: int = 100):
    """
    Получение всех заявок на регистрацию, отсортированных по дате создания (сначала новые)
    """
    return db.query(RegistrationRequest).order_by(desc(RegistrationRequest.created_at)).offset(skip).limit(limit).all()

def get_registration_request(db: Session, request_id: int):
    """
    Получение заявки на регистрацию по ID
    """
    return db.query(RegistrationRequest).filter(RegistrationRequest.id == request_id).first()

def get_pending_registration_requests(db: Session, skip: int = 0, limit: int = 100):
    """
    Получение заявок на регистрацию в статусе "ожидает"
    """
    return db.query(RegistrationRequest).filter(RegistrationRequest.status == "ожидает").order_by(desc(RegistrationRequest.created_at)).offset(skip).limit(limit).all()

def update_registration_request_status(db: Session, request_id: int, request_update: RegistrationRequestUpdate):
    """
    Обновление статуса заявки на регистрацию
    """
    db_request = db.query(RegistrationRequest).filter(RegistrationRequest.id == request_id).first()
    if not db_request:
        return None
    
    # Проверяем, что заявка еще не обработана
    if db_request.status != "ожидает":
        return None
    
    # Обновляем статус и время обработки
    db_request.status = request_update.status
    db_request.comment = request_update.comment
    db_request.processed_at = datetime.now()
    
    # Если заявка одобрена, активируем пользователя
    if request_update.status == "одобрено":
        user = db.query(User).filter(User.id == db_request.user_id).first()
        if user:
            user.is_active = True
            user.role = db_request.requested_role  # Устанавливаем запрошенную роль
    
    db.commit()
    db.refresh(db_request)
    return db_request