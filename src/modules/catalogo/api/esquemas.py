import uuid
from decimal import Decimal

from pydantic import BaseModel, Field


class CriarProdutoRequest(BaseModel):
    nome: str
    preco: Decimal = Field(gt=0)
    ativo: bool = True


class CriarIngredienteRequest(BaseModel):
    nome: str
    quantidade_estoque: Decimal = Field(ge=0)
    valor: Decimal = Field(ge=0)
    estoque_minimo: Decimal = Field(ge=0)


class VincularComposicaoRequest(BaseModel):
    ingrediente_id: uuid.UUID
    quantidade: Decimal = Field(gt=0)


class ProdutoResponse(BaseModel):
    id: uuid.UUID
    nome: str
    preco: Decimal
    ativo: bool


class IngredienteResponse(BaseModel):
    id: uuid.UUID
    nome: str
    quantidade_estoque: Decimal
    valor: Decimal
    estoque_minimo: Decimal