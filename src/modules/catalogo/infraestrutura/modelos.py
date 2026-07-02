import uuid

from sqlalchemy import ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database import Base


class ProdutoModel(Base):
    __tablename__ = "produtos"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    nome: Mapped[str]
    preco: Mapped[float] = mapped_column(Numeric(10, 2))
    ativo: Mapped[bool] = mapped_column(default=True)

    composicao: Mapped[list["ComposicaoItemModel"]] = relationship(
        back_populates="produto", lazy="selectin"
    )


class IngredienteModel(Base):
    __tablename__ = "ingredientes"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    nome: Mapped[str]
    quantidade_estoque: Mapped[float] = mapped_column(Numeric(10, 3))
    valor: Mapped[float] = mapped_column(Numeric(10, 2))
    estoque_minimo: Mapped[float] = mapped_column(Numeric(10, 3))


class ComposicaoItemModel(Base):
    __tablename__ = "composicao_itens"
    __table_args__ = (UniqueConstraint("produto_id", "ingrediente_id"),)

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    produto_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("produtos.id", ondelete="CASCADE"))
    ingrediente_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("ingredientes.id", ondelete="RESTRICT"))
    quantidade: Mapped[float] = mapped_column(Numeric(10, 3))

    produto: Mapped["ProdutoModel"] = relationship(back_populates="composicao")
    ingrediente: Mapped["IngredienteModel"] = relationship(lazy="joined")


class ComboModel(Base):
    __tablename__ = "combos"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    nome: Mapped[str]
    desconto: Mapped[float] = mapped_column(Numeric(10, 2))

    itens: Mapped[list["ComboProdutoModel"]] = relationship(lazy="selectin")


class ComboProdutoModel(Base):
    __tablename__ = "combo_produtos"
    __table_args__ = (UniqueConstraint("combo_id", "produto_id"),)

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    combo_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("combos.id", ondelete="CASCADE"))
    produto_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("produtos.id", ondelete="RESTRICT"))
    quantidade: Mapped[int] = mapped_column(default=1)

    produto: Mapped["ProdutoModel"] = relationship(lazy="selectin")