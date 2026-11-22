import pytest
from fastapi.testclient import TestClient

from app import database
from app.main import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    """Cada teste usa seu próprio banco SQLite temporário."""
    monkeypatch.setattr(database, "DATABASE_PATH", tmp_path / "teste_produtos.db")
    with TestClient(app) as test_client:
        yield test_client


def criar_payload(**alteracoes):
    payload = {"nome": "Teclado", "preco": 149.90, "quantidade": 12}
    payload.update(alteracoes)
    return payload


def test_cadastrar_produto_valido(client):
    resposta = client.post("/produtos", json=criar_payload())

    assert resposta.status_code == 201
    assert resposta.json() == {
        "id": 1,
        "nome": "Teclado",
        "preco": 149.90,
        "quantidade": 12,
    }


def test_listar_produtos_cadastrados(client):
    client.post("/produtos", json=criar_payload())
    client.post("/produtos", json=criar_payload(nome="Mouse"))

    resposta = client.get("/produtos")

    assert resposta.status_code == 200
    assert [produto["nome"] for produto in resposta.json()] == ["Teclado", "Mouse"]


def test_filtrar_produtos_por_nome_sem_diferenciar_maiusculas(client):
    client.post("/produtos", json=criar_payload(nome="Teclado mecânico"))
    client.post("/produtos", json=criar_payload(nome="Suporte para teclado"))
    client.post("/produtos", json=criar_payload(nome="Mouse"))

    resposta = client.get("/produtos", params={"nome": "TECLADO"})

    assert resposta.status_code == 200
    assert [produto["nome"] for produto in resposta.json()] == [
        "Teclado mecânico",
        "Suporte para teclado",
    ]


def test_consultar_produto_por_id(client):
    criado = client.post("/produtos", json=criar_payload()).json()

    resposta = client.get(f"/produtos/{criado['id']}")

    assert resposta.status_code == 200
    assert resposta.json() == criado


def test_atualizar_produto_existente(client):
    criado = client.post("/produtos", json=criar_payload()).json()
    dados_atualizados = criar_payload(nome="Teclado mecânico", preco=299.99, quantidade=5)

    resposta = client.put(f"/produtos/{criado['id']}", json=dados_atualizados)

    assert resposta.status_code == 200
    assert resposta.json() == {"id": criado["id"], **dados_atualizados}


def test_excluir_produto_existente(client):
    criado = client.post("/produtos", json=criar_payload()).json()

    resposta = client.delete(f"/produtos/{criado['id']}")

    assert resposta.status_code == 204
    assert client.get(f"/produtos/{criado['id']}").status_code == 404


@pytest.mark.parametrize(
    "alteracoes",
    [
        {"preco": -0.01},
        {"quantidade": -1},
        {"nome": ""},
    ],
    ids=["preco-negativo", "quantidade-negativa", "nome-vazio"],
)
def test_rejeitar_dados_invalidos(client, alteracoes):
    resposta = client.post("/produtos", json=criar_payload(**alteracoes))

    assert resposta.status_code == 422


def test_consultar_produto_inexistente_retorna_404(client):
    resposta = client.get("/produtos/9999")

    assert resposta.status_code == 404
    assert resposta.json()["detail"] == "Produto não encontrado"
