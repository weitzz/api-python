from sqlalchemy import Column, Integer, String, Boolean, Float

from core.configs import settings


class UsuarioModel(settings.DBBaseModel):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(256), nullable=True)
    email = Column(String(256), nullable=False, index=True, unique=True)
    password = Column(String(256), nullable=False)
    refresh_token = Column(String(256), nullable=True)

