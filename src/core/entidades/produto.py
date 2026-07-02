from dataclasses import dataclass, field
from decimal import Decimal
from uuid import UUID

from src.core.entidades.composicao_item import ComposicaoItem


@dataclass
class Produto:
    id: UUID
    nome: str
    preco: Decimal
    ativo: bool = True
    composicao: list[ComposicaoItem] = field(default_factory=list)

    def calcular_preco(self) -> Decimal:
        return self.preco

    def get_composicao(self) -> list[ComposicaoItem]:
        return self.composicao
