import os
from pathlib import Path

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, ConfigDict, EmailStr
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import declarative_base, relationship, selectinload, sessionmaker

app = FastAPI(title="API de clientes")

database_path = Path(os.environ.get("DATABASE_PATH", "instance/clientes.sqlite3"))
database_path.parent.mkdir(parents=True, exist_ok=True)
engine = create_engine(
    f"sqlite:///{database_path.as_posix()}",
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    telefone = Column(String, nullable=False, default="")
    endereco = relationship(
        "Endereco",
        back_populates="cliente",
        uselist=False,
        cascade="all, delete-orphan",
    )


class Endereco(Base):
    __tablename__ = "enderecos"

    id = Column(Integer, primary_key=True)
    cliente_id = Column(
        Integer,
        ForeignKey("clientes.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    logradouro = Column(String, nullable=False)
    numero = Column(String, nullable=False)
    complemento = Column(String, nullable=False, default="")
    bairro = Column(String, nullable=False)
    cidade = Column(String, nullable=False)
    estado = Column(String(2), nullable=False)
    cep = Column(String, nullable=False)
    cliente = relationship("Cliente", back_populates="endereco")


class EnderecoSchema(BaseModel):
    logradouro: str
    numero: str
    complemento: str = ""
    bairro: str
    cidade: str
    estado: str
    cep: str


class ClienteSchema(BaseModel):
    nome: str
    email: EmailStr
    telefone: str = ""
    endereco: EnderecoSchema


class ClienteResponse(ClienteSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int


Base.metadata.create_all(bind=engine)


def buscar_cliente(session, cliente_id):
    return (
        session.query(Cliente)
        .options(selectinload(Cliente.endereco))
        .filter(Cliente.id == cliente_id)
        .first()
    )


def montar_cliente(dados):
    return Cliente(
        nome=dados.nome,
        email=str(dados.email),
        telefone=dados.telefone,
        endereco=Endereco(
            logradouro=dados.endereco.logradouro,
            numero=dados.endereco.numero,
            complemento=dados.endereco.complemento,
            bairro=dados.endereco.bairro,
            cidade=dados.endereco.cidade,
            estado=dados.endereco.estado.upper(),
            cep=dados.endereco.cep,
        ),
    )


@app.get("/api/clientes", response_model=list[ClienteResponse])
def listar_clientes():
    with SessionLocal() as session:
        return session.query(Cliente).options(selectinload(Cliente.endereco)).order_by(Cliente.nome).all()


@app.get("/api/clientes/{cliente_id}", response_model=ClienteResponse)
def obter_cliente(cliente_id: int):
    with SessionLocal() as session:
        cliente = buscar_cliente(session, cliente_id)
        if cliente is None:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        return cliente


@app.post("/api/clientes", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
def criar_cliente(dados: ClienteSchema):
    with SessionLocal() as session:
        cliente = montar_cliente(dados)
        session.add(cliente)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            raise HTTPException(status_code=409, detail="Já existe um cliente com este e-mail")
        session.refresh(cliente)
        return buscar_cliente(session, cliente.id)


@app.put("/api/clientes/{cliente_id}", response_model=ClienteResponse)
def atualizar_cliente(cliente_id: int, dados: ClienteSchema):
    with SessionLocal() as session:
        cliente = buscar_cliente(session, cliente_id)
        if cliente is None:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        cliente.nome = dados.nome
        cliente.email = str(dados.email)
        cliente.telefone = dados.telefone
        cliente.endereco.logradouro = dados.endereco.logradouro
        cliente.endereco.numero = dados.endereco.numero
        cliente.endereco.complemento = dados.endereco.complemento
        cliente.endereco.bairro = dados.endereco.bairro
        cliente.endereco.cidade = dados.endereco.cidade
        cliente.endereco.estado = dados.endereco.estado.upper()
        cliente.endereco.cep = dados.endereco.cep
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            raise HTTPException(status_code=409, detail="Já existe outro cliente com este e-mail")
        return buscar_cliente(session, cliente_id)


@app.delete("/api/clientes/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_cliente(cliente_id: int):
    with SessionLocal() as session:
        cliente = buscar_cliente(session, cliente_id)
        if cliente is None:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        session.delete(cliente)
        session.commit()
