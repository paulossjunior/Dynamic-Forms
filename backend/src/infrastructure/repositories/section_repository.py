from typing import List, Optional
from sqlalchemy.orm import Session
from models import Section as SectionModel
from src.application.ports.section_repository import ISectionRepository
from src.domain.entities.section import Section as SectionEntity
from src.infrastructure.mappers.section_mapper import SectionMapper


class SectionRepository(ISectionRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, section: SectionEntity) -> SectionEntity:
        db_section = SectionMapper.to_model(section)
        self.db.add(db_section)
        self.db.commit()
        self.db.refresh(db_section)
        return SectionMapper.to_entity(db_section)

    def get_by_id(self, section_id: int) -> Optional[SectionEntity]:
        db_section = (
            self.db.query(SectionModel).filter(SectionModel.id == section_id).first()
        )
        if db_section:
            return SectionMapper.to_entity(db_section)
        return None

    def list_by_form(self, form_id: int) -> List[SectionEntity]:
        db_sections = (
            self.db.query(SectionModel)
            .filter(SectionModel.form_id == form_id)
            .order_by(SectionModel.order_index)
            .all()
        )
        return [SectionMapper.to_entity(s) for s in db_sections]

    def update(self, section: SectionEntity) -> SectionEntity:
        db_section = (
            self.db.query(SectionModel).filter(SectionModel.id == section.id).first()
        )
        if not db_section:
            raise ValueError(f"Section {section.id} not found")

        db_section.name = section.name
        db_section.description = section.description
        db_section.order_index = section.order

        self.db.commit()
        self.db.refresh(db_section)
        return SectionMapper.to_entity(db_section)

    def delete(self, section_id: int) -> None:
        db_section = (
            self.db.query(SectionModel).filter(SectionModel.id == section_id).first()
        )
        if db_section:
            self.db.delete(db_section)
            self.db.commit()
