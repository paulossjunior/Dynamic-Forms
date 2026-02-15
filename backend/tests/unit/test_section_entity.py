import pytest
from src.domain.entities.section import Section

def test_section_creation_with_valid_data():
    # Arrange
    section = Section(
        id=1,
        name="Personal Information",
        description="Fields related to person identity",
        order=0,
        form_id=1
    )
    
    # Assert
    assert section.id == 1
    assert section.name == "Personal Information"
    assert section.description == "Fields related to person identity"
    assert section.order == 0
    assert section.form_id == 1

def test_section_validation_fails_with_empty_name():
    # Arrange
    section = Section(id=None, name="", description=None, order=0, form_id=1)
    
    # Act & Assert
    with pytest.raises(ValueError, match="Section name is required and must be <= 100 chars"):
        section.validate()

def test_section_validation_fails_with_long_name():
    # Arrange
    long_name = "A" * 101
    section = Section(id=None, name=long_name, description=None, order=0, form_id=1)
    
    # Act & Assert
    with pytest.raises(ValueError, match="Section name is required and must be <= 100 chars"):
        section.validate()

def test_section_validation_fails_with_long_description():
    # Arrange
    long_desc = "A" * 501
    section = Section(id=None, name="Valid Name", description=long_desc, order=0, form_id=1)
    
    # Act & Assert
    with pytest.raises(ValueError, match="Section description must be <= 500 chars"):
        section.validate()

def test_section_validation_fails_with_negative_order():
    # Arrange
    section = Section(id=None, name="Valid Name", description=None, order=-1, form_id=1)
    
    # Act & Assert
    with pytest.raises(ValueError, match="Section order must be >= 0"):
        section.validate()
