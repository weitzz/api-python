from typing import Optional

from pydantic import BaseModel as SCBaseModel


class MedicamentoSchema(SCBaseModel):
    id: Optional[int]
    nome: str
    preco: float
    data_de_validade: str
    imagem: str
    estoque: Optional[bool]
    quantidade: Optional[str]

    class Config:
        orm_mode = True

