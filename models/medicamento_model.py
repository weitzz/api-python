from sqlalchemy import Column, Integer, String, Date
from core.configs import settings


class MedicamentoModel(settings.DBBaseModel):
    __tablename__ = 'medicamentos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(256))
    preco = Column()
    data_de_validade = Column(Date)
    imagem = Column(String)
