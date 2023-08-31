# from sqlalchemy import Column, Integer, String, ForeignKey
# from sqlalchemy.orm import relationship
#
# from core.configs import settings
#
#
# class ImageModel(settings.DBBaseModel):
#     __tablename__ = 'imagem'
#     id = Column(Integer, primary_key=True, index=True)
#     filename = Column(String)
#     medicamento = relationship("MedicamentoModel", back_populates="imagem_medicamento")
#
