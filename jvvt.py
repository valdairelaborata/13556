from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
 
Base = declarative_base()
 
class Cliente(Base):
    __tablename__ = 'clientes'
 
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    endereco_id = Column(Integer, ForeignKey('endereco_cliente.id'))
    endereco = relationship('EnderecoCliente', back_populates='clientes')

    emprestimos = relationship('Emprestimo', back_populates='cliente')

 
class EnderecoCliente(Base):
    __tablename__ = 'endereco_cliente'
 
    id = Column(Integer, primary_key=True)
    rua = Column(String, nullable=False)
    numero = Column(String, nullable=False)
    clientes = relationship('Cliente', back_populates='endereco')
 
class Biblioteca(Base):
    __tablename__ = 'biblioteca'
 
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    localização = Column(String, nullable=False, unique=True)

class StatusEmprestimo(Base):
    __tablename__ = 'status_emprestimo'

    id = Column(Integer, primary_key=True)
    status = Column(String, nullable=False, unique=True)

    emprestimos = relationship('Emprestimo', back_populates='status')


class Livro(Base):
    __tablename__ = 'livro'

    id = Column(Integer, primary_key=True)
    nome_livro = Column(String, nullable=False, unique=True)
    preco = Column(Integer, nullable=False)
    descricao = Column(String, nullable=False)
    categoria = Column(String, nullable=False)

    emprestimos = relationship('Emprestimo', back_populates='livro')

class Emprestimo(Base):
    __tablename__ = 'emprestimo'
 
    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'))
    cliente = relationship('Cliente', back_populates='emprestimos')

    status_id = Column(Integer, ForeignKey('status_emprestimo.id'))
    status = relationship('StatusEmprestimo', back_populates='emprestimos') 

    livro_id = Column(Integer, ForeignKey('livro.id'))
    livro = relationship('Livro', back_populates='emprestimos')

    # clientes = relationship('Cliente', back_populates='emprestimo')
 

