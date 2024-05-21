from typing import Optional

from pydantic import BaseModel as SCBaseModel
from datetime import date


class MedicamentoSchema(SCBaseModel):
    id: Optional[int]
    nome: str
    preco: float
    data_de_validade: str
    imagem: str
    quantidade: Optional[float]

    class Config:
        orm_mode = True


class MedicamentoUpdateSchema(MedicamentoSchema):
    id: Optional[int]
    nome: Optional[str]
    preco: Optional[float]
    data_de_validade: Optional[str]
    imagem: Optional[str]
    quantidade: Optional[float]
