from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    telefone = Column(String, nullable=False, default="")
    enderecos = relationship(
        "Endereco",
        back_populates="cliente",
        cascade="all, delete-orphan",
    )
