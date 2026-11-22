from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProdutoCriacao(BaseModel):
    nome: str = Field(min_length=1, description="Nome do produto")
    preco: float = Field(
        ge=0,
        allow_inf_nan=False,
        description="Preço do produto, maior ou igual a zero",
    )
    quantidade: int = Field(ge=0, description="Quantidade em estoque, maior ou igual a zero")

    @field_validator("nome")
    @classmethod
    def nome_nao_pode_ser_apenas_espacos(cls, valor: str) -> str:
        nome = valor.strip()
        if not nome:
            raise ValueError("O nome não pode estar vazio")
        return nome


class Produto(ProdutoCriacao):
    id: int
    model_config = ConfigDict(from_attributes=True)
