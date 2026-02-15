from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.section import Section


class ISectionRepository(ABC):
    @abstractmethod
    def create(self, section: Section) -> Section:
        pass

    @abstractmethod
    def get_by_id(self, section_id: int) -> Optional[Section]:
        pass

    @abstractmethod
    def list_by_form(self, form_id: int) -> List[Section]:
        pass

    @abstractmethod
    def update(self, section: Section) -> Section:
        pass

    @abstractmethod
    def delete(self, section_id: int) -> None:
        pass
