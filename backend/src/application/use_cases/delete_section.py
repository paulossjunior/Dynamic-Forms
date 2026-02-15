from src.application.ports.section_repository import ISectionRepository


class DeleteSection:
    def __init__(self, repository: ISectionRepository):
        self.repository = repository

    def execute(self, section_id: int) -> None:
        return self.repository.delete(section_id)
