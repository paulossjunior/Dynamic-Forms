import pytest
from unittest.mock import MagicMock
from src.application.use_cases.create_section import CreateSection
from src.application.dtos.section_dto import CreateSectionDTO
from src.application.ports.section_repository import ISectionRepository
from src.domain.entities.section import Section

def test_create_section_use_case():
    # Arrange
    mock_repo = MagicMock(spec=ISectionRepository)
    dto = CreateSectionDTO(
        name="Test Section",
        description="Test Desc",
        order=1,
        form_id=10
    )
    
    # Mock behavior: return a Section entity with an ID
    def side_effect(section):
        section.id = 1
        return section
    mock_repo.create.side_effect = side_effect
    
    use_case = CreateSection(mock_repo)
    
    # Act
    result = use_case.execute(dto)
    
    # Assert
    assert result.id == 1
    assert result.name == "Test Section"
    assert result.form_id == 10
    mock_repo.create.assert_called_once()
    # Check if a Section entity was passed to create
    args, _ = mock_repo.create.call_args
    assert isinstance(args[0], Section)
    assert args[0].name == "Test Section"
