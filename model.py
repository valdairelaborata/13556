
from sqlalchemy import Column, ForeignKey,  Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Cliente(Base):
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True) 
    endereco_id = Column(Integer, ForeignKey('enderecos.id')) 
    endereco = relationship("Endereco", back_populates="clientes")
    


class Endereco(Base):
    __tablename__ = 'enderecos'

    id = Column(Integer, primary_key=True)
    rua = Column(String, nullable=False)
    numero = Column(String, nullable=False)
    clientes = relationship("Cliente", back_populates="endereco")
    
