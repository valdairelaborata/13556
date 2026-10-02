from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
 
Base = declarative_base()
 
SQLALCHEMY_DATABASE_URL = 'sqlite:///database.db'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
 
Base.metadata.create_all(engine)
 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()
 
class Cliente(Base):
    __tablename__ = 'clientes'
 
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    endereco_id = Column(Integer, ForeignKey('endereco_cliente.id'), nullable=False)
    endereco = relationship('EnderecoCliente', back_populates='clientes')
    emprestimo = relationship('Emprestimo', back_populates='cliente')
 
class EnderecoCliente(Base):
    __tablename__ = 'endereco_cliente'
 
    id = Column(Integer, primary_key=True)
    rua = Column(String, nullable=False)
    numero = Column(String, nullable=False)
    clientes = relationship('Cliente', back_populates='endereco')
 
class Livro(Base):
    __tablename__ = 'livro'
 
    id = Column(Integer, primary_key=True)
    nome_livro = Column(String, nullable=False, unique=True)
    preco = Column(Integer, nullable=False)
    descricao = Column(String, nullable=False)
    categoria = Column(String, nullable=False)
    emprestimo = relationship('Emprestimo', back_populates='livro')
 
class Emprestimo(Base):
    __tablename__ = 'emprestimo'
 
    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'))
    cliente = relationship('Cliente', back_populates='emprestimo')
    livro_id = Column(Integer, ForeignKey('livro.id'))
    livro = relationship('Livro', back_populates='emprestimo')
    status_id = Column(Integer, ForeignKey('status.id'))
    status = relationship('Status', back_populates='emprestimo')
 
class Status(Base):
    __tablename__ = 'status'
 
    id = Column(Integer, primary_key=True)
    status = Column(String, nullable=False)
    emprestimo = relationship('Emprestimo', back_populates='status')