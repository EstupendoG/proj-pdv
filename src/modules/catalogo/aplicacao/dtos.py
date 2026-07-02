import uuid
from dataclasses import dataclass
from decimal import Decimal

@dataclass
class CriarProdutoDTO:
    nome: str
    preco: Decimal
    ativo: bool = True

@dataclass
class CriarIngredienteDTO:
    nome: str
    quantidade_estoque: Decimal
    valor: Decimal
    estoque_minimo: Decimal

@dataclass
class VincularComposicaoDTO:
    produto_id: uuid.UUID
    ingrediente_id: uuid.UUID
    quantidade: Decimal