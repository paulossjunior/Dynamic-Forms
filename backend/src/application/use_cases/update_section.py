from src.application.ports.section_repository import ISectionRepository
from src.application.dtos.section_dto import UpdateSectionDTO
from src.domain.entities.section import Section


class UpdateSection:
    def __init__(self, repository: ISectionRepository):
        self.repository = repository

    def execute(self, section_id: int, dto: UpdateSectionDTO) -> Section:
        section = self.repository.get_by_id(section_id)
        if not section:
            raise ValueError(f"Section with id {section_id} not found")

        if dto.name is not None:
            section.name = dto.name
        if dto.description is not None:
            section.description = dto.description
        if dto.order is not None:
            section.order = dto.order

        section.validate()
        return self.repository.update(section)
