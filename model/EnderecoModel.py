

from sqlalchemy import Column, ForeignKey,  Integer, String
from produto_model import Base


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

class Endereco(Base):
    __tablename__ = 'enderecos'

    id = Column(Integer, primary_key=True)
    rua = Column(String, nullable=False)
    numero = Column(String, nullable=False)
    clientes = relationship("Cliente", back_populates="endereco")
    
