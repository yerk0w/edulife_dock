# app/services/__init__.py
"""
Инициализация сервисов
"""
from .document import get_documents, get_document, get_user_documents, create_document, update_document_status
from .user import get_user, get_user_by_username, get_user_by_email, get_users, create_user, authenticate_user, update_user, change_user_password
from .registration_request import get_registration_requests, get_registration_request, get_pending_registration_requests, update_registration_request_status
from .template import get_templates, get_template, get_templates_by_role, create_template, update_template, delete_template

__all__ = [
    "get_documents", "get_document", "get_user_documents", "create_document", "update_document_status",
    "get_user", "get_user_by_username", "get_user_by_email", "get_users", "create_user", "authenticate_user", "update_user", "change_user_password",
    "get_registration_requests", "get_registration_request", "get_pending_registration_requests", "update_registration_request_status",
    "get_templates", "get_template", "get_templates_by_role", "create_template", "update_template", "delete_template"
]