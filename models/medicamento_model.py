from sqlalchemy import Column, Integer, String, Date, Float
from core.configs import settings


class MedicamentoModel(settings.DBBaseModel):
    __tablename__ = 'medicamentos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(256))
    preco = Column(Float)
    data_de_validade = Column(String(256))
    imagem = Column(String)
