import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.infrastructure.database import get_db
from src.modules.catalogo.api.esquemas import (
    CriarIngredienteRequest,
    CriarProdutoRequest,
    IngredienteResponse,
    ProdutoResponse,
    VincularComposicaoRequest,
)
from src.modules.catalogo.aplicacao.casos_uso import (
    VincularComposicaoUseCase,
    CriarIngredientesUseCase,
    CriarProdutosUseCase,
)
from src.modules.catalogo.aplicacao.dtos import (
    CriarIngredienteDTO,
    CriarProdutoDTO,
    VincularComposicaoDTO,
)
from src.modules.catalogo.infraestrutura.repositorios import (
    IngredienteRepositorySQLAlchemy,
    ProdutoRepositorySQLAlchemy,
)

router = APIRouter(prefix="/produtos", tags=["catalogo"])
router_ingredientes = APIRouter(prefix="/ingredientes", tags=["catalogo"])


@router.post("", response_model=ProdutoResponse, status_code=201)
def criar_produto(payload: CriarProdutoRequest, sessao: Session = Depends(get_db)):
    repositorio = ProdutoRepositorySQLAlchemy(sessao)
    use_case = CriarProdutosUseCase(repositorio)
    produto = use_case.executar(CriarProdutoDTO(**payload.model_dump()))
    return ProdutoResponse(id=produto.id, nome=produto.nome, preco=produto.preco, ativo=produto.ativo)


@router_ingredientes.post("", response_model=IngredienteResponse, status_code=201)
def criar_ingrediente(payload: CriarIngredienteRequest, sessao: Session = Depends(get_db)):
    repositorio = IngredienteRepositorySQLAlchemy(sessao)
    use_case = CriarIngredientesUseCase(repositorio)
    ingrediente = use_case.executar(CriarIngredienteDTO(**payload.model_dump()))
    return IngredienteResponse(
        id=ingrediente.id,
        nome=ingrediente.nome,
        quantidade_estoque=ingrediente.quantidade_estoque,
        valor=ingrediente.valor,
        estoque_minimo=ingrediente.estoque_minimo,
    )


@router.post("/{produto_id}/composicao", status_code=204)
def vincular_composicao(
    produto_id: uuid.UUID, payload: VincularComposicaoRequest, sessao: Session = Depends(get_db)
):
    repositorio_produto = ProdutoRepositorySQLAlchemy(sessao)
    repositorio_ingrediente = IngredienteRepositorySQLAlchemy(sessao)
    use_case = VincularComposicaoUseCase(sessao, repositorio_produto, repositorio_ingrediente)
    use_case.executar(
        VincularComposicaoDTO(
            produto_id=produto_id,
            ingrediente_id=payload.ingrediente_id,
            quantidade=payload.quantidade,
        )
    )