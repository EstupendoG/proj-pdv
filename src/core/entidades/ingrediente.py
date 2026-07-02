from dataclasses import dataclass, field
from decimal import Decimal
from uuid import UUID
import uuid

from src.core.excecoes.estoque import EstoqueInsuficienteError


@dataclass
class Ingrediente:
    nome: str
    quantidade_estoque: Decimal
    valor: Decimal
    estoque_minimo: Decimal
    id: UUID = field(default_factory=uuid.uuid4)

    def baixar(self, qtd: Decimal) -> None:
        if qtd > self.quantidade_estoque:
            raise EstoqueInsuficienteError(
                f"Estoque insuficiente de {self.nome}: "
                f"solicitado {qtd}, disponível {self.quantidade_estoque}"
            )
        self.quantidade_estoque -= qtd
