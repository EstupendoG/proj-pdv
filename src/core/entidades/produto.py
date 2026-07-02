from dataclasses import dataclass, field
from decimal import Decimal
from uuid import UUID
import uuid

from src.core.entidades.composicao_item import ComposicaoItem


@dataclass
class Produto:
    nome: str
    preco: Decimal
    ativo: bool = True
    composicao: list[ComposicaoItem] = field(default_factory=list)
    id: UUID = field(default_factory=uuid.uuid4)
    

    def calcular_preco(self) -> Decimal:
        return self.preco

    def get_composicao(self) -> list[ComposicaoItem]:
        return self.composicao
