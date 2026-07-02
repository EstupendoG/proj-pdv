from src.core.entidades.combo import Combo
from src.core.entidades.composicao_item import ComposicaoItem
from src.core.entidades.ingrediente import Ingrediente
from src.core.entidades.produto import Produto
from src.modules.catalogo.infraestrutura.modelos import ComboModel, ProdutoModel


def ingrediente_para_dominio(model) -> Ingrediente:
    return Ingrediente(
        id=model.id,
        nome=model.nome,
        quantidade_estoque=model.quantidade_estoque,
        valor=model.valor,
        estoque_minimo=model.estoque_minimo,
    )


def produto_para_dominio(model: ProdutoModel) -> Produto:
    composicao = [
        ComposicaoItem(
            ingrediente=ingrediente_para_dominio(ci.ingrediente),
            quantidade=ci.quantidade,
        )
        for ci in model.composicao
    ]
    return Produto(id=model.id, nome=model.nome, preco=model.preco, ativo=model.ativo, composicao=composicao)


def combo_para_dominio(model: ComboModel) -> Combo:
    produtos = [produto_para_dominio(item.produto) for item in model.itens]
    return Combo(id=model.id, nome=model.nome, desconto=model.desconto, itens=produtos)