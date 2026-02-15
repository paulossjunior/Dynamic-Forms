from dataclasses import dataclass
from typing import Optional


@dataclass
class Section:
    """
    Representa uma seção lógica dentro de um formulário.

    Regras de Negócio:
    - Nome é obrigatório (max 100 chars)
    - Descrição é opcional (max 500 chars)
    - Ordem deve ser única dentro do formulário
    """

    id: Optional[int]
    name: str
    description: Optional[str]
    order: int
    form_id: int

    def validate(self) -> None:
        """Valida regras de negócio da seção"""
        if not self.name or len(self.name) > 100:
            raise ValueError("Section name is required and must be <= 100 chars")
        if self.description and len(self.description) > 500:
            raise ValueError("Section description must be <= 500 chars")
        if self.order < 0:
            raise ValueError("Section order must be >= 0")
