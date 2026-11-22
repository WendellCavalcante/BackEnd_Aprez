from contextlib import asynccontextmanager
from pathlib import Path
import sqlite3

from fastapi import FastAPI, HTTPException, Response, status

from .database import criar_tabela, obter_conexao
from .schemas import Produto, ProdutoCriacao


@asynccontextmanager
async def lifespan(app: FastAPI):
    criar_tabela()
    yield


app = FastAPI(
    title="API de Produtos",
    description="API REST para cadastro e gerenciamento de produtos.",
    version="1.0.0",
    lifespan=lifespan,
)


def buscar_produto(produto_id: int) -> dict:
    with obter_conexao() as conexao:
        linha = conexao.execute(
            "SELECT id, nome, preco, quantidade FROM produtos WHERE id = ?",
            (produto_id,),
        ).fetchone()
    if linha is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return dict(linha)


@app.get("/produtos", response_model=list[Produto], tags=["Produtos"])
def listar_produtos(nome: str | None = None):
    with obter_conexao() as conexao:
        linhas = conexao.execute(
            "SELECT id, nome, preco, quantidade FROM produtos ORDER BY id"
        ).fetchall()
    produtos = [dict(linha) for linha in linhas]
    if nome is None:
        return produtos
    termo = nome.casefold()
    return [produto for produto in produtos if termo in produto["nome"].casefold()]


@app.get("/produtos/{produto_id}", response_model=Produto, tags=["Produtos"])
def obter_produto(produto_id: int):
    return buscar_produto(produto_id)


@app.post(
    "/produtos",
    response_model=Produto,
    status_code=status.HTTP_201_CREATED,
    tags=["Produtos"],
)
def criar_produto(dados: ProdutoCriacao):
    with obter_conexao() as conexao:
        cursor = conexao.execute(
            "INSERT INTO produtos (nome, preco, quantidade) VALUES (?, ?, ?)",
            (dados.nome, dados.preco, dados.quantidade),
        )
        produto_id = cursor.lastrowid
    return buscar_produto(produto_id)


@app.put("/produtos/{produto_id}", response_model=Produto, tags=["Produtos"])
def atualizar_produto(produto_id: int, dados: ProdutoCriacao):
    buscar_produto(produto_id)
    with obter_conexao() as conexao:
        conexao.execute(
            "UPDATE produtos SET nome = ?, preco = ?, quantidade = ? WHERE id = ?",
            (dados.nome, dados.preco, dados.quantidade, produto_id),
        )
    return buscar_produto(produto_id)


@app.delete(
    "/produtos/{produto_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Produtos"],
)
def excluir_produto(produto_id: int):
    buscar_produto(produto_id)
    with obter_conexao() as conexao:
        conexao.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
    return Response(status_code=status.HTTP_204_NO_CONTENT)
