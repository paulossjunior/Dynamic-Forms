from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Json
from datetime import date

class CustomFieldDefinitionBase(BaseModel):
    entity_type: str
    key_name: str
    label: str
    field_type: str
    options: Json[List[str]] = '[]'  # Defaults to empty list in JSON string format
    validation_rules: Json[Dict[str, Any]] = '{}'  # Defaults to empty dict in JSON string format
    is_active: bool = True

class CustomFieldDefinitionCreate(CustomFieldDefinitionBase):
    pass

class CustomFieldDefinition(CustomFieldDefinitionBase):
    id: int

    class Config:
        from_attributes = True

class PersonBase(BaseModel):
    name: str
    email: str
    custom_data: Json[Dict[str, Any]] = '{}'  # Dynamic fields data

class PersonCreate(PersonBase):
    pass

class Person(PersonBase):
    id: int
    
    class Config:
        from_attributes = True

# Form Schemas
class FormBase(BaseModel):
    name: str
    description: Optional[str] = None

class FormFieldLinkInput(BaseModel):
    field_id: int
    is_required: bool = False

class FormCreate(FormBase):
    fields: List[FormFieldLinkInput] = []

class FormFieldAssociation(BaseModel):
    field_id: int
    order: int
    is_required: bool
    field: CustomFieldDefinition

    class Config:
        from_attributes = True

class Form(FormBase):
    id: int
    fields: List[FormFieldAssociation] = []

    class Config:
        from_attributes = True
