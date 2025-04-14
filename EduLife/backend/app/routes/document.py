from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.document import DocumentCreate, DocumentResponse, DocumentUpdate
from app.services.document import get_documents, get_document, get_user_documents, create_document, update_document_status
from app.security.jwt import get_current_active_user, get_admin_user, get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/documents",
    tags=["documents"],
)

@router.post("/", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
def create_document_route(
    document: DocumentCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Создание нового документа
    """
    return create_document(db=db, document=document, user_id=current_user.id)

@router.get("/", response_model=List[DocumentResponse])
def read_documents(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Получение всех документов (для администраторов) или документов пользователя
    """
    if current_user.role == "админ":
        documents = get_documents(db, skip=skip, limit=limit)
    else:
        documents = get_user_documents(db, user_id=current_user.id, skip=skip, limit=limit)
    
    # Добавляем имя автора для каждого документа
    for doc in documents:
        doc.author_name = doc.author.full_name
    
    return documents

@router.get("/all", response_model=List[DocumentResponse])
def read_all_documents(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """
    Получение всех документов (только для администраторов)
    """
    documents = get_documents(db, skip=skip, limit=limit)
    
    # Добавляем имя автора для каждого документа
    for doc in documents:
        doc.author_name = doc.author.full_name
    
    return documents

@router.get("/{document_id}", response_model=DocumentResponse)
def read_document(
    document_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Получение документа по ID
    """
    db_document = get_document(db, document_id=document_id)
    if db_document is None:
        raise HTTPException(status_code=404, detail="Документ не найден")
    
    # Проверяем права доступа (админ или автор документа)
    if current_user.role != "админ" and db_document.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Нет доступа к этому документу")
    
    # Добавляем имя автора
    db_document.author_name = db_document.author.full_name
    
    return db_document

@router.patch("/{document_id}/review", response_model=DocumentResponse)
def review_document(
    document_id: int, 
    document_update: DocumentUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """
    Изменение статуса документа (только для администраторов)
    """
    db_document = update_document_status(db, document_id=document_id, document_update=document_update)
    if db_document is None:
        raise HTTPException(status_code=404, detail="Документ не найден")
    
    # Добавляем имя автора
    db_document.author_name = db_document.author.full_name
    
    return db_document