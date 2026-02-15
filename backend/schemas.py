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

# Section Schemas
class SectionBase(BaseModel):
    name: str
    description: Optional[str] = None
    order_index: int = 0
    form_id: int

class SectionCreate(BaseModel):
    name: str
    description: Optional[str] = None
    order_index: int = 0
    # form_id is optional here because it will be assigned when the form is created
    form_id: Optional[int] = None 
    temp_id: Optional[str] = None # For linking fields in the same request

class Section(SectionBase):
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
    section_id: Optional[int] = None
    section_temp_id: Optional[str] = None # To link to a section being created in the same request

class FormCreate(FormBase):
    fields: List[FormFieldLinkInput] = []
    sections: List[SectionCreate] = []

class FormFieldAssociation(BaseModel):
    field_id: int
    order: int
    is_required: bool
    section_id: Optional[int] = None
    field: CustomFieldDefinition

    class Config:
        from_attributes = True

class Form(FormBase):
    id: int
    fields: List[FormFieldAssociation] = []
    sections: List[Section] = []

    class Config:
        from_attributes = True

