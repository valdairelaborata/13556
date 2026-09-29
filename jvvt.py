from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
 
Base = declarative_base()
 
DATABASE_URL = 'sqlite:///jvvt.db'
engine = create_engine(DATABASE_URL)
 
Base.metadata.create_all(engine)
 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()
 
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

class Emprestimo(Base):
    __tablename__ = 'emprestimo'
 
    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'))
    cliente = relationship('Cliente', back_populates='emprestimos')

    status_id = Column(Integer, ForeignKey('status_emprestimo.id'))
    status = relationship('StatusEmprestimo', back_populates='emprestimos') 

    # clientes = relationship('Cliente', back_populates='emprestimo')
    # livro_id = Column(Integer, ForeignKey('livro.id'))
    # livro = relationship('Livro', back_populates='emprestimo')
 
# class Livro(Base):
#     __tablename__ = 'livro'
 
#     id = Column(Integer, primary_key=True)
#     nome_livro = Column(String, nullable = False,  unique = True)
#     preco = Column(Integer, nullable = False)
#     descricao = Column(String, nullable = False)
#     categoria = Column(String, nullable = False)
#     disponibilidade = Column(String, nullable = False, default = 'Disponível')


 
Base.metadata.create_all(engine)
 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()
 
novo_cliente =  Cliente(nome = 'Jvvtvvt', email = 'jvvt@gmail.com')
db.add(novo_cliente)
db.commit()
 
# novo_enderecocliente = EnderecoCliente(rua='Rua XV de Novembro', numero='1234')
# db.add(novo_enderecocliente)
# db.commit()
 
# novo_biblioteca = Biblioteca(nome='Biblioteca do jvvt', localização='Rua do jvvt')
# db.add(novo_biblioteca)
# db.commit()
 
# novo_emprestimo = Emprestimo(cliente_id=novo_cliente.id, livro_id=1)
# db.add(novo_emprestimo)
# db.commit()
 
# novo_livro = Livro(nome_livro='O pequeno principe', preco = 199,
# descricao = 'Livro famoso no qual até foi homenageado com um hospital em seu nome', categoria = 'Infantil', disponibilidade = 'Disponível')
# db.add(novo_livro)
# db.commit()
 
# novo_livro = Livro(nome_livro='Dom casmurro', preco = 49,
# descricao = 'Romance escrito por Machado de Assis', categoria = 'Romance', disponibilidade = 'Disponível')
# db.add(novo_livro)
# db.commit()
 
# novo_livro = Livro(nome_livro='Os anjos contam historias', preco = 89,
# descricao = 'Romance escrito por Machado de Assis', categoria = 'Romance', disponibilidade = 'Indisponível')
# db.add(novo_livro)
# db.commit()
 