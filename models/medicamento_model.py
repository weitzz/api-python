from sqlalchemy import Column, Integer, String, Boolean, Float, Date

from core.configs import settings


class MedicamentoModel(settings.DBBaseModel):
    __tablename__ = 'medicamentos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(256))
    preco = Column(Float)
    data_de_validade = Column(String)
    imagem = Column(String)
    quantidade = Column(Float)
