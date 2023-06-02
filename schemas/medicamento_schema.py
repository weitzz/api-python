from typing import Optional
from pydantic import BaseModel as SCBaseModel


class MedicamentoSchema(SCBaseModel):
    id: Optional[int]
    nome: str
    preco: str
    data_de_validade: str
    imagem: str

    class Config:
        orm_mode = True
