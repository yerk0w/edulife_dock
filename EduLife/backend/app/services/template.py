import os
import shutil
from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.template import Template
from app.schemas.template import TemplateCreate, TemplateUpdate

# Путь для сохранения загруженных шаблонов
TEMPLATES_DIR = os.path.join(os.getcwd(), "app", "static", "templates")

# Создаем директорию, если она не существует
os.makedirs(TEMPLATES_DIR, exist_ok=True)

def get_templates(db: Session, skip: int = 0, limit: int = 100):
    """
    Получение всех шаблонов документов
    """
    return db.query(Template).order_by(desc(Template.created_at)).offset(skip).limit(limit).all()

def get_template(db: Session, template_id: int):
    """
    Получение шаблона по ID
    """
    return db.query(Template).filter(Template.id == template_id).first()

def get_templates_by_role(db: Session, role: str, skip: int = 0, limit: int = 100):
    """
    Получение шаблонов, доступных для определенной роли
    """
    query = db.query(Template)
    
    if role == "студент":
        query = query.filter(Template.available_for_students == True)
    elif role == "преподаватель":
        query = query.filter(Template.available_for_teachers == True)
    # Для админа доступны все шаблоны
    
    return query.order_by(desc(Template.created_at)).offset(skip).limit(limit).all()

async def create_template(db: Session, template: TemplateCreate, file: UploadFile):
    """
    Создание нового шаблона документа
    """
    # Проверяем тип файла (должен быть PDF)
    if not file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Файл должен быть в формате PDF"
        )
    
    # Генерируем уникальное имя файла
    file_name = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}"
    file_path = os.path.join(TEMPLATES_DIR, file_name)
    
    # Сохраняем файл
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Создаем запись в БД
    db_template = Template(
        name=template.name,
        description=template.description,
        file_path=f"/static/templates/{file_name}",  # Относительный путь для доступа через веб
        available_for_students=template.available_for_students,
        available_for_teachers=template.available_for_teachers
    )
    
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    
    return db_template

def update_template(db: Session, template_id: int, template_update: TemplateUpdate):
    """
    Обновление шаблона документа
    """
    db_template = db.query(Template).filter(Template.id == template_id).first()
    if not db_template:
        return None
    
    # Обновляем только переданные поля
    update_data = template_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_template, key, value)
    
    db.commit()
    db.refresh(db_template)
    return db_template

def delete_template(db: Session, template_id: int):
    """
    Удаление шаблона документа
    """
    db_template = db.query(Template).filter(Template.id == template_id).first()
    if not db_template:
        return False
    
    # Удаляем файл с диска
    file_path = os.path.join(os.getcwd(), "app", db_template.file_path.lstrip('/'))
    if os.path.exists(file_path):
        os.remove(file_path)
    
    # Удаляем запись из БД
    db.delete(db_template)
    db.commit()
    
    return True