from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from src.core.excecoes.estoque import EstoqueInsuficienteError


@dataclass
class Ingrediente:
    id: UUID
    nome: str
    quantidade_estoque: Decimal
    valor: Decimal
    estoque_minimo: Decimal

    def baixar(self, qtd: Decimal) -> None:
        if qtd > self.quantidade_estoque:
            raise EstoqueInsuficienteError(
                f"Estoque insuficiente de {self.nome}: "
                f"solicitado {qtd}, disponível {self.quantidade_estoque}"
            )
        self.quantidade_estoque -= qtd
