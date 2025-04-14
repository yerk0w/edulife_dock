from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.document import Document
from app.models.user import User
from app.schemas.document import DocumentCreate, DocumentUpdate

def get_documents(db: Session, skip: int = 0, limit: int = 100):
    """
    Получение всех документов
    """
    return db.query(Document).order_by(desc(Document.created_at)).offset(skip).limit(limit).all()

def get_document(db: Session, document_id: int):
    """
    Получение документа по ID
    """
    return db.query(Document).filter(Document.id == document_id).first()

def get_user_documents(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    """
    Получение документов пользователя
    """
    return db.query(Document).filter(Document.author_id == user_id).order_by(desc(Document.created_at)).offset(skip).limit(limit).all()

def create_document(db: Session, document: DocumentCreate, user_id: int):
    """
    Создание нового документа
    """
    db_document = Document(
        title=document.title,
        content=document.content,
        author_id=user_id,
        template_type=document.template_type
    )
    
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    
    return db_document

def update_document_status(db: Session, document_id: int, document_update: DocumentUpdate):
    """
    Обновление статуса документа
    """
    db_document = db.query(Document).filter(Document.id == document_id).first()
    if not db_document:
        return None
    
    db_document.status = document_update.status
    db.commit()
    db.refresh(db_document)
    
    return db_document