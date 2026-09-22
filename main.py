import os
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine, inspect, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import declarative_base, relationship, selectinload, sessionmaker, Session


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
	enderecos = relationship(
		"Endereco",
		back_populates="cliente",
		cascade="all, delete-orphan",
	)


class Endereco(Base):
	__tablename__ = "enderecos"

	id = Column(Integer, primary_key=True)
	cliente_id = Column(Integer, ForeignKey("clientes.id", ondelete="CASCADE"), nullable=False)
	logradouro = Column(String, nullable=False)
	numero = Column(String, nullable=False)
	complemento = Column(String, nullable=False, default="")
	bairro = Column(String, nullable=False)
	cidade = Column(String, nullable=False)
	estado = Column(String(2), nullable=False)
	cep = Column(String, nullable=False)
	cliente = relationship("Cliente", back_populates="enderecos")


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
	enderecos: list[EnderecoSchema] = Field(default_factory=list)


class ClienteResponse(ClienteSchema):
	model_config = ConfigDict(from_attributes=True)
	id: int


def get_db():
	session = SessionLocal()
	try:
		yield session
	finally:
		session.close()


def migrate_enderecos_table():
	if "enderecos" not in inspect(engine).get_table_names():
		return

	with engine.connect() as connection:
		indexes = connection.execute(text("PRAGMA index_list('enderecos')")).mappings().all()
		unique_cliente_id = any(
			index["unique"]
			and [
				column["name"]
				for column in connection.execute(
					text(f"PRAGMA index_info('{index['name']}')")
				).mappings().all()
			] == ["cliente_id"]
			for index in indexes
		)

	if not unique_cliente_id:
		return

	with engine.begin() as connection:
		connection.execute(text("ALTER TABLE enderecos RENAME TO enderecos_antiga"))

	Base.metadata.create_all(bind=engine)

	with engine.begin() as connection:
		connection.execute(
			text(
				"""
				INSERT INTO enderecos
				(id, cliente_id, logradouro, numero, complemento, bairro, cidade, estado, cep)
				SELECT id, cliente_id, logradouro, numero, complemento, bairro, cidade, estado, cep
				FROM enderecos_antiga
				"""
			)
		)
		connection.execute(text("DROP TABLE enderecos_antiga"))


def initialize_database():
	migrate_enderecos_table()
	Base.metadata.create_all(bind=engine)


def buscar_cliente(session: Session, cliente_id: int):
	return (
		session.query(Cliente)
		.options(selectinload(Cliente.enderecos))
		.filter(Cliente.id == cliente_id)
		.first()
	)


def criar_enderecos(dados: ClienteSchema):
	return [
		Endereco(
			logradouro=endereco.logradouro,
			numero=endereco.numero,
			complemento=endereco.complemento,
			bairro=endereco.bairro,
			cidade=endereco.cidade,
			estado=endereco.estado.upper(),
			cep=endereco.cep,
		)
		for endereco in dados.enderecos
	]


app = FastAPI(title="API de clientes")


@app.get("/api/clientes", response_model=list[ClienteResponse])
def listar_clientes(session: Session = Depends(get_db)):
	return (
		session.query(Cliente)
		.options(selectinload(Cliente.enderecos))
		.order_by(Cliente.nome)
		.all()
	)


@app.get("/api/clientes/{cliente_id}", response_model=ClienteResponse)
def obter_cliente(cliente_id: int, session: Session = Depends(get_db)):
	cliente = buscar_cliente(session, cliente_id)
	if cliente is None:
		raise HTTPException(status_code=404, detail="Cliente não encontrado")
	return cliente


@app.post("/api/clientes", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
def criar_cliente(dados: ClienteSchema, session: Session = Depends(get_db)):
	cliente = Cliente(
		nome=dados.nome,
		email=str(dados.email),
		telefone=dados.telefone,
		enderecos=criar_enderecos(dados),
	)
	session.add(cliente)
	try:
		session.commit()
	except IntegrityError as error:
		session.rollback()
		raise HTTPException(status_code=409, detail="Já existe um cliente com este e-mail") from error
	session.refresh(cliente)
	return buscar_cliente(session, cliente.id)


@app.put("/api/clientes/{cliente_id}", response_model=ClienteResponse)
def atualizar_cliente(cliente_id: int, dados: ClienteSchema, session: Session = Depends(get_db)):
	cliente = buscar_cliente(session, cliente_id)
	if cliente is None:
		raise HTTPException(status_code=404, detail="Cliente não encontrado")

	cliente.nome = dados.nome
	cliente.email = str(dados.email)
	cliente.telefone = dados.telefone
	cliente.enderecos = criar_enderecos(dados)
	try:
		session.commit()
	except IntegrityError as error:
		session.rollback()
		raise HTTPException(status_code=409, detail="Já existe outro cliente com este e-mail") from error
	return buscar_cliente(session, cliente_id)


@app.delete("/api/clientes/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_cliente(cliente_id: int, session: Session = Depends(get_db)):
	cliente = buscar_cliente(session, cliente_id)
	if cliente is None:
		raise HTTPException(status_code=404, detail="Cliente não encontrado")
	session.delete(cliente)
	session.commit()


initialize_database()
