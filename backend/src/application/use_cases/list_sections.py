from src.application.ports.section_repository import ISectionRepository
from src.domain.entities.section import Section
from typing import List


class ListSections:
    def __init__(self, repository: ISectionRepository):
        self.repository = repository

    def execute(self, form_id: int) -> List[Section]:
        return self.repository.list_by_form(form_id)
