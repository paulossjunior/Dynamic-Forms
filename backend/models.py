from sqlalchemy import Boolean, Column, Integer, String, Text, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import json

class CustomFieldDefinition(Base):
    __tablename__ = "custom_field_definitions"

    id = Column(Integer, primary_key=True, index=True)
    entity_type = Column(String, index=True) # 'person' or 'address'
    key_name = Column(String, index=True)
    label = Column(String)
    field_type = Column(String) # 'text', 'number', 'select', 'multiselect', 'checkbox', 'radio'
    options = Column(Text, default="[]") # JSON array of options
    validation_rules = Column(Text, default="{}") # JSON object for validation rules
    is_active = Column(Boolean, default=True)

    __table_args__ = (
        UniqueConstraint('entity_type', 'key_name', name='uix_definitions_entity_key'),
    )

class FormDefinition(Base):
    __tablename__ = "forms"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    
    # Relationships
    fields = relationship("FormFields", back_populates="form", cascade="all, delete-orphan")
    sections = relationship("Section", back_populates="form", cascade="all, delete-orphan", order_by="Section.order_index")

class Section(Base):
    __tablename__ = "sections"
    id = Column(Integer, primary_key=True, index=True)
    form_id = Column(Integer, ForeignKey("forms.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    order_index = Column(Integer, default=0)

    form = relationship("FormDefinition", back_populates="sections")
    fields = relationship("FormFields", back_populates="section")


class FormFields(Base):
    __tablename__ = "form_fields"
    form_id = Column(Integer, ForeignKey('forms.id'), primary_key=True)
    field_id = Column(Integer, ForeignKey('custom_field_definitions.id'), primary_key=True)
    section_id = Column(Integer, ForeignKey('sections.id'), nullable=True)
    is_required = Column(Boolean, default=False)
    order = Column(Integer, default=0)
    
    form = relationship("FormDefinition", back_populates="fields")
    field = relationship("CustomFieldDefinition")
    section = relationship("Section", back_populates="fields")


class Person(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    # Storing custom data as a JSON string in a TEXT column
    custom_data = Column(Text, default="{}")
