# app/scripts/__init__.py

from .create_templates import main as create_templates, create_application_template, create_reference_template, create_permission_slip_template

__all__ = [
    "create_templates",
    "create_application_template", 
    "create_reference_template", 
    "create_permission_slip_template"
]