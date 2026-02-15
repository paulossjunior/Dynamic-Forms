from pydantic import BaseModel, Field
from typing import Optional


class CreateSectionDTO(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    order: int = Field(ge=0)
    form_id: int


class UpdateSectionDTO(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    order: Optional[int] = Field(None, ge=0)


class SectionResponseDTO(BaseModel):
    id: int
    name: str
    description: Optional[str]
    order: int
    form_id: int
    field_count: int = 0  # Default to 0, will be implementation specific
