
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Produto(Base):
    __tablename__ = 'produtos'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    preco = Column(Float, nullable=False)