from src.application.ports.section_repository import ISectionRepository
from src.application.dtos.section_dto import CreateSectionDTO
from src.domain.entities.section import Section


class CreateSection:
    def __init__(self, repository: ISectionRepository):
        self.repository = repository

    def execute(self, dto: CreateSectionDTO) -> Section:
        section = Section(
            id=None,
            name=dto.name,
            description=dto.description,
            order=dto.order,
            form_id=dto.form_id,
        )

        section.validate()
        return self.repository.create(section)
