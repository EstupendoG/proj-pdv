from decimal import Decimal
from uuid import uuid4

import pytest

from src.core.entidades.combo import Combo
from src.core.entidades.composicao_item import ComposicaoItem
from src.core.entidades.ingrediente import Ingrediente
from src.core.entidades.produto import Produto
from src.core.excecoes.estoque import EstoqueInsuficienteError


def _ingrediente(nome: str, estoque: str = "10.000") -> Ingrediente:
    return Ingrediente(
        id=uuid4(),
        nome=nome,
        quantidade_estoque=Decimal(estoque),
        valor=Decimal("1.00"),
        estoque_minimo=Decimal("1.000"),
    )


def _produto(
    nome: str, preco: str, composicao: list[ComposicaoItem] | None = None
) -> Produto:
    return Produto(
        id=uuid4(),
        nome=nome,
        preco=Decimal(preco),
        composicao=composicao or [],
    )


@pytest.mark.unit
def test_produto_calcula_preco_simples() -> None:
    produto = _produto("X-Burger", "15.90")

    assert produto.calcular_preco() == Decimal("15.90")


@pytest.mark.unit
def test_combo_soma_preco_dos_itens() -> None:
    combo = Combo(
        id=uuid4(),
        nome="Combo Família",
        desconto=Decimal("0"),
        itens=[
            _produto("X-Burger", "15.00"),
            _produto("Batata", "8.00"),
        ],
    )

    assert combo.calcular_preco() == Decimal("23.00")


@pytest.mark.unit
def test_combo_aplica_desconto_corretamente() -> None:
    combo = Combo(
        id=uuid4(),
        nome="Combo Família",
        desconto=Decimal("3.00"),
        itens=[
            _produto("X-Burger", "15.00"),
            _produto("Batata", "8.00"),
        ],
    )

    assert combo.calcular_preco() == Decimal("20.00")


@pytest.mark.unit
def test_combo_nao_retorna_preco_negativo() -> None:
    combo = Combo(
        id=uuid4(),
        nome="Combo Promocional",
        desconto=Decimal("50.00"),
        itens=[_produto("Suco", "5.00")],
    )

    assert combo.calcular_preco() == Decimal("0")


@pytest.mark.unit
def test_combo_get_composicao_agrega_ingredientes_dos_produtos() -> None:
    carne = _ingrediente("Carne")
    queijo = _ingrediente("Queijo")
    batata = _ingrediente("Batata")

    burger = _produto(
        "X-Burger",
        "15.00",
        [
            ComposicaoItem(ingrediente=carne, quantidade=Decimal("0.150")),
            ComposicaoItem(ingrediente=queijo, quantidade=Decimal("0.030")),
        ],
    )
    porcao_batata = _produto(
        "Batata",
        "8.00",
        [ComposicaoItem(ingrediente=batata, quantidade=Decimal("0.200"))],
    )
    combo = Combo(
        id=uuid4(),
        nome="Combo Família",
        desconto=Decimal("0"),
        itens=[burger, porcao_batata],
    )

    composicao = combo.get_composicao()

    assert len(composicao) == 3
    assert composicao[0].ingrediente.nome == "Carne"
    assert composicao[1].ingrediente.nome == "Queijo"
    assert composicao[2].ingrediente.nome == "Batata"


@pytest.mark.unit
def test_ingrediente_baixa_estoque_com_sucesso() -> None:
    ingrediente = _ingrediente("Carne", "5.000")

    ingrediente.baixar(Decimal("2.000"))

    assert ingrediente.quantidade_estoque == Decimal("3.000")


@pytest.mark.unit
def test_ingrediente_baixa_estoque_insuficiente_lanca_excecao() -> None:
    ingrediente = _ingrediente("Carne", "1.000")

    with pytest.raises(EstoqueInsuficienteError):
        ingrediente.baixar(Decimal("2.000"))
