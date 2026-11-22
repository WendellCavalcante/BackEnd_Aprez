# API de gerenciamento de produtos

API REST construída com FastAPI, Pydantic e SQLite para cadastrar, consultar, atualizar e remover produtos.

## Requisitos

- Python 3.10 ou superior
- `pip`

## Instalação e execução

No terminal, na pasta do projeto:

```bash
python -m venv .venv
```

Ative o ambiente virtual:

```bash
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Linux/macOS
source .venv/bin/activate
```

Instale as dependências e inicie o servidor:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

A API estará em `http://127.0.0.1:8000`. A documentação interativa Swagger fica em `http://127.0.0.1:8000/docs` (e a documentação alternativa em `/redoc`). O arquivo `produtos.db` e a tabela são criados automaticamente ao iniciar a aplicação.

## Endpoints

| Método | Caminho | Ação | Resposta |
|---|---|---|---|
| GET | `/produtos` | Lista os produtos | `200 OK` |
| GET | `/produtos/{id}` | Consulta um produto | `200 OK` ou `404 Not Found` |
| POST | `/produtos` | Cria um produto | `201 Created` |
| PUT | `/produtos/{id}` | Substitui os dados de um produto | `200 OK` ou `404 Not Found` |
| DELETE | `/produtos/{id}` | Remove um produto | `204 No Content` ou `404 Not Found` |

Erros de validação retornam `422 Unprocessable Entity`. Nome vazio ou composto apenas por espaços, preço negativo e quantidade negativa são rejeitados.

## Exemplo de criação

```json
{
  "nome": "Teclado",
  "preco": 149.9,
  "quantidade": 12
}
```

O `id` é gerado automaticamente pelo banco e não deve ser enviado no corpo da criação ou atualização. O `PUT` atualiza todos os campos do produto.
