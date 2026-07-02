from decimal import Decimal
import pytest
from fastapi.testclient import TestClient

from src.infrastructure.database import get_db
from src.main import app


def _client_com_sessao(sessao_db):
    app.dependency_overrides[get_db] = lambda: sessao_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_criar_produto(sessao_db):
    client = next(_client_com_sessao(sessao_db))
    resposta = client.post("/produtos", json={"nome": "X-Burguer", "preco": "15.00"})
    
    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["nome"] == "X-Burguer"
    assert Decimal(corpo["preco"]) == Decimal("15.00")


def test_criar_ingrediente(sessao_db):
    client = next(_client_com_sessao(sessao_db))
    resposta = client.post(
        "/ingredientes",
        json={"nome": "Pão", "quantidade_estoque": "100", "valor": "1.00", "estoque_minimo": "10"},
    )
    assert resposta.status_code == 201
    assert resposta.json()["nome"] == "Pão"


def test_vincular_composicao(sessao_db):
    client = next(_client_com_sessao(sessao_db))
    
    # Cria o produto e o ingrediente para poder vinculá-los
    produto = client.post("/produtos", json={"nome": "X-Salada", "preco": "17.00"}).json()
    ingrediente = client.post(
        "/ingredientes",
        json={"nome": "Queijo", "quantidade_estoque": "50", "valor": "2.00", "estoque_minimo": "5"},
    ).json()

    # Vincula o ingrediente ao produto
    resposta = client.post(
        f"/produtos/{produto['id']}/composicao",
        json={"ingrediente_id": ingrediente["id"], "quantidade": "2"},
    )
    assert resposta.status_code == 204