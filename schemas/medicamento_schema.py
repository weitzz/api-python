
from typing import Optional
from pydantic import BaseModel as SCBaseModel
from pydantic.datetime_parse import datetime



class MedicamentoSchema(SCBaseModel):
    id: Optional[int]
    nome: str
    preco: float
    data_de_validade: str
    imagem: str

    class Config:
        orm_mode = True
