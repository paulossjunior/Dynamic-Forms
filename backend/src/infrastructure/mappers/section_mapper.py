from src.domain.entities.section import Section as SectionEntity
from models import Section as SectionModel


class SectionMapper:
    @staticmethod
    def to_entity(model: SectionModel) -> SectionEntity:
        return SectionEntity(
            id=model.id,
            name=model.name,
            description=model.description,
            order=model.order_index,
            form_id=model.form_id,
        )

    @staticmethod
    def to_model(entity: SectionEntity) -> SectionModel:
        return SectionModel(
            id=entity.id,
            form_id=entity.form_id,
            name=entity.name,
            description=entity.description,
            order_index=entity.order,
        )
