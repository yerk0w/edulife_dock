from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from pydantic import parse_obj_as

from app.db.database import get_db
from app.schemas.template import TemplateResponse, TemplateCreate, TemplateUpdate
from app.services.template import get_templates, get_template, get_templates_by_role, create_template, update_template, delete_template
from app.security.jwt import get_current_active_user, get_admin_user
from app.models.user import User

router = APIRouter(
    prefix="/templates",
    tags=["templates"],
)

@router.get("/", response_model=List[TemplateResponse])
def read_templates(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Получение шаблонов, доступных для текущего пользователя
    """
    return get_templates_by_role(db, current_user.role, skip=skip, limit=limit)

@router.get("/all", response_model=List[TemplateResponse])
def read_all_templates(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """
    Получение всех шаблонов (только для администраторов)
    """
    return get_templates(db, skip=skip, limit=limit)

@router.get("/{template_id}", response_model=TemplateResponse)
def read_template(
    template_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Получение шаблона по ID
    """
    db_template = get_template(db, template_id=template_id)
    if db_template is None:
        raise HTTPException(status_code=404, detail="Шаблон не найден")
    
    # Проверяем доступ пользователя к шаблону
    if current_user.role == "студент" and not db_template.available_for_students:
        raise HTTPException(status_code=403, detail="Нет доступа к этому шаблону")
    elif current_user.role == "преподаватель" and not db_template.available_for_teachers:
        raise HTTPException(status_code=403, detail="Нет доступа к этому шаблону")
    
    return db_template

@router.post("/", response_model=TemplateResponse, status_code=status.HTTP_201_CREATED)
async def upload_template(
    name: str = Form(...),
    description: str = Form(None),
    available_for_students: bool = Form(True),
    available_for_teachers: bool = Form(True),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """
    Загрузка нового шаблона (только для администраторов)
    """
    template_data = {
        "name": name,
        "description": description,
        "available_for_students": available_for_students,
        "available_for_teachers": available_for_teachers
    }
    template = parse_obj_as(TemplateCreate, template_data)
    return await create_template(db, template, file)

@router.put("/{template_id}", response_model=TemplateResponse)
def update_template_info(
    template_id: int,
    template_update: TemplateUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """
    Обновление информации о шаблоне (только для администраторов)
    """
    db_template = update_template(db, template_id=template_id, template_update=template_update)
    if db_template is None:
        raise HTTPException(status_code=404, detail="Шаблон не найден")
    return db_template

@router.delete("/{template_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_template_by_id(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """
    Удаление шаблона (только для администраторов)
    """
    success = delete_template(db, template_id=template_id)
    if not success:
        raise HTTPException(status_code=404, detail="Шаблон не найден")
    return None