from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from src.core.entidades.ingrediente import Ingrediente


@dataclass
class ComposicaoItem:
    ingrediente: Ingrediente
    quantidade: Decimal
