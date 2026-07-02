from dataclasses import dataclass, field
from decimal import Decimal
from uuid import UUID

from src.core.entidades.composicao_item import ComposicaoItem
from src.core.entidades.produto import Produto


@dataclass
class Combo:
    id: UUID
    nome: str
    desconto: Decimal
    itens: list[Produto] = field(default_factory=list)

    def calcular_preco(self) -> Decimal:
        total = sum(produto.calcular_preco() for produto in self.itens)
        preco_final = total - self.desconto
        return max(preco_final, Decimal("0"))

    def get_composicao(self) -> list[ComposicaoItem]:
        composicao: list[ComposicaoItem] = []
        for produto in self.itens:
            composicao.extend(produto.get_composicao())
        return composicao
