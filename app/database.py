import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator


DATABASE_PATH = Path(__file__).resolve().parent.parent / "produtos.db"


@contextmanager
def obter_conexao() -> Iterator[sqlite3.Connection]:
    conexao = sqlite3.connect(DATABASE_PATH)
    conexao.row_factory = sqlite3.Row
    try:
        with conexao:
            yield conexao
    finally:
        conexao.close()


def criar_tabela() -> None:
    with obter_conexao() as conexao:
        conexao.execute(
            """
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL CHECK (length(trim(nome)) > 0),
                preco REAL NOT NULL CHECK (preco >= 0),
                quantidade INTEGER NOT NULL CHECK (quantidade >= 0)
            )
            """
        )
