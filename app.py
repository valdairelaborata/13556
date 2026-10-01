from collections.abc import Generator
import logging
import os

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import create_engine, func, inspect, text
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

from jvvt import Base, Biblioteca, Cliente, Emprestimo, EnderecoCliente, Livro, StatusEmprestimo

logger = logging.getLogger(__name__)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///jvvt.db").strip()
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite:") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)
with engine.begin() as connection:
    if inspect(connection).has_table("livro"):
        livro_columns = {column["name"] for column in inspect(connection).get_columns("livro")}
        if "disponibilidade" in livro_columns:
            connection.exec_driver_sql("ALTER TABLE livro DROP COLUMN disponibilidade")
    if inspect(connection).has_table("emprestimo"):
        emprestimo_columns = {column["name"] for column in inspect(connection).get_columns("emprestimo")}
        if "livro_id" not in emprestimo_columns:
            connection.exec_driver_sql("ALTER TABLE emprestimo ADD COLUMN livro_id INTEGER REFERENCES livro(id)")

app = FastAPI(
    title="API da Biblioteca",
    description="API para gerenciar clientes, endereços, bibliotecas, empréstimos e livros.",
    version="1.0.0",
    openapi_tags=[
        {"name": "Geral", "description": "Informações gerais da API."},
        {"name": "Clientes", "description": "Cadastro e consulta de clientes."},
        {"name": "Endereços", "description": "Endereços vinculados aos clientes."},
        {"name": "Bibliotecas", "description": "Cadastro e consulta de bibliotecas."},
        {"name": "Status de empréstimos", "description": "Situações possíveis para empréstimos."},
        {"name": "Empréstimos", "description": "Criação e gerenciamento de empréstimos."},
        {"name": "Livros", "description": "Catálogo, disponibilidade e empréstimos de livros."},
    ],
)
OPEN_LOAN_STATUSES = ("aberto", "em aberto")


@app.exception_handler(SQLAlchemyError)
async def handle_database_error(request: Request, error: SQLAlchemyError) -> JSONResponse:
    logger.error(
        "Erro de banco de dados em %s %s",
        request.method,
        request.url.path,
        exc_info=(type(error), error, error.__traceback__),
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Erro interno ao acessar o banco de dados"},
    )


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def save_record(db: Session, record: object) -> object:
    try:
        db.add(record)
        db.commit()
        db.refresh(record)
        return record
    except IntegrityError as error:
        db.rollback()
        raise HTTPException(status_code=409, detail="Conflito com dados existentes ou relacionados") from error


def get_record(db: Session, model: type, record_id: int, resource_name: str) -> object:
    record = db.get(model, record_id)
    if record is None:
        raise HTTPException(status_code=404, detail=f"{resource_name} não encontrado")
    return record


def delete_record(db: Session, record: object) -> None:
    try:
        db.delete(record)
        db.commit()
    except IntegrityError as error:
        db.rollback()
        raise HTTPException(status_code=409, detail="Registro possui dados relacionados") from error


def emprestimo_em_aberto():
    return Emprestimo.status.has(
        func.lower(func.trim(StatusEmprestimo.status)).in_(OPEN_LOAN_STATUSES)
    )


class ORMResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ClienteInput(BaseModel):
    nome: str
    email: str
    endereco_id: int | None = None


class ClienteOutput(ClienteInput, ORMResponse):
    id: int


class EnderecoInput(BaseModel):
    rua: str
    numero: str


class EnderecoOutput(EnderecoInput, ORMResponse):
    id: int


class BibliotecaInput(BaseModel):
    nome: str
    localizacao: str


class BibliotecaOutput(ORMResponse):
    id: int
    nome: str
    localizacao: str = Field(validation_alias="localização")


class StatusInput(BaseModel):
    status: str


class StatusOutput(StatusInput, ORMResponse):
    id: int


class EmprestimoInput(BaseModel):
    cliente_id: int | None = None
    status_id: int | None = None
    livro_id: int | None = None


class EmprestimoOutput(EmprestimoInput, ORMResponse):
    id: int


class LivroInput(BaseModel):
    nome_livro: str
    preco: int
    descricao: str
    categoria: str


class LivroOutput(LivroInput, ORMResponse):
    id: int


@app.get("/", tags=["Geral"])
def read_root() -> dict[str, str]:
    return {"message": "API da Biblioteca"}


@app.get("/clientes", response_model=list[ClienteOutput], tags=["Clientes"])
def listar_clientes(db: Session = Depends(get_db)) -> list[Cliente]:
    return db.query(Cliente).all()


@app.post("/clientes", response_model=ClienteOutput, status_code=201, tags=["Clientes"])
def criar_cliente(dados: ClienteInput, db: Session = Depends(get_db)) -> Cliente:
    return save_record(db, Cliente(**dados.model_dump()))


@app.get("/clientes/{cliente_id}", response_model=ClienteOutput, tags=["Clientes"])
def buscar_cliente(cliente_id: int, db: Session = Depends(get_db)) -> Cliente:
    return get_record(db, Cliente, cliente_id, "Cliente")


@app.put("/clientes/{cliente_id}", response_model=ClienteOutput, tags=["Clientes"])
def atualizar_cliente(cliente_id: int, dados: ClienteInput, db: Session = Depends(get_db)) -> Cliente:
    cliente = get_record(db, Cliente, cliente_id, "Cliente")
    for campo, valor in dados.model_dump().items():
        setattr(cliente, campo, valor)
    return save_record(db, cliente)


@app.delete("/clientes/{cliente_id}", status_code=204, tags=["Clientes"])
def excluir_cliente(cliente_id: int, db: Session = Depends(get_db)) -> None:
    delete_record(db, get_record(db, Cliente, cliente_id, "Cliente"))


@app.get("/enderecos", response_model=list[EnderecoOutput], tags=["Endereços"])
def listar_enderecos(db: Session = Depends(get_db)) -> list[EnderecoCliente]:
    return db.query(EnderecoCliente).all()


@app.post("/enderecos", response_model=EnderecoOutput, status_code=201, tags=["Endereços"])
def criar_endereco(dados: EnderecoInput, db: Session = Depends(get_db)) -> EnderecoCliente:
    return save_record(db, EnderecoCliente(**dados.model_dump()))


@app.get("/enderecos/{endereco_id}", response_model=EnderecoOutput, tags=["Endereços"])
def buscar_endereco(endereco_id: int, db: Session = Depends(get_db)) -> EnderecoCliente:
    return get_record(db, EnderecoCliente, endereco_id, "Endereço")


@app.put("/enderecos/{endereco_id}", response_model=EnderecoOutput, tags=["Endereços"])
def atualizar_endereco(endereco_id: int, dados: EnderecoInput, db: Session = Depends(get_db)) -> EnderecoCliente:
    endereco = get_record(db, EnderecoCliente, endereco_id, "Endereço")
    for campo, valor in dados.model_dump().items():
        setattr(endereco, campo, valor)
    return save_record(db, endereco)


@app.delete("/enderecos/{endereco_id}", status_code=204, tags=["Endereços"])
def excluir_endereco(endereco_id: int, db: Session = Depends(get_db)) -> None:
    delete_record(db, get_record(db, EnderecoCliente, endereco_id, "Endereço"))


@app.get("/bibliotecas", response_model=list[BibliotecaOutput], tags=["Bibliotecas"])
def listar_bibliotecas(db: Session = Depends(get_db)) -> list[Biblioteca]:
    return db.query(Biblioteca).all()


@app.post("/bibliotecas", response_model=BibliotecaOutput, status_code=201, tags=["Bibliotecas"])
def criar_biblioteca(dados: BibliotecaInput, db: Session = Depends(get_db)) -> Biblioteca:
    return save_record(db, Biblioteca(nome=dados.nome, localização=dados.localizacao))


@app.get("/bibliotecas/{biblioteca_id}", response_model=BibliotecaOutput, tags=["Bibliotecas"])
def buscar_biblioteca(biblioteca_id: int, db: Session = Depends(get_db)) -> Biblioteca:
    return get_record(db, Biblioteca, biblioteca_id, "Biblioteca")


@app.put("/bibliotecas/{biblioteca_id}", response_model=BibliotecaOutput, tags=["Bibliotecas"])
def atualizar_biblioteca(biblioteca_id: int, dados: BibliotecaInput, db: Session = Depends(get_db)) -> Biblioteca:
    biblioteca = get_record(db, Biblioteca, biblioteca_id, "Biblioteca")
    biblioteca.nome = dados.nome
    biblioteca.localização = dados.localizacao
    return save_record(db, biblioteca)


@app.delete("/bibliotecas/{biblioteca_id}", status_code=204, tags=["Bibliotecas"])
def excluir_biblioteca(biblioteca_id: int, db: Session = Depends(get_db)) -> None:
    delete_record(db, get_record(db, Biblioteca, biblioteca_id, "Biblioteca"))


@app.get("/status-emprestimos", response_model=list[StatusOutput], tags=["Status de empréstimos"])
def listar_status(db: Session = Depends(get_db)) -> list[StatusEmprestimo]:
    return db.query(StatusEmprestimo).all()


@app.post("/status-emprestimos", response_model=StatusOutput, status_code=201, tags=["Status de empréstimos"])
def criar_status(dados: StatusInput, db: Session = Depends(get_db)) -> StatusEmprestimo:
    return save_record(db, StatusEmprestimo(**dados.model_dump()))


@app.get("/status-emprestimos/{status_id}", response_model=StatusOutput, tags=["Status de empréstimos"])
def buscar_status(status_id: int, db: Session = Depends(get_db)) -> StatusEmprestimo:
    return get_record(db, StatusEmprestimo, status_id, "Status")


@app.put("/status-emprestimos/{status_id}", response_model=StatusOutput, tags=["Status de empréstimos"])
def atualizar_status(status_id: int, dados: StatusInput, db: Session = Depends(get_db)) -> StatusEmprestimo:
    status_registro = get_record(db, StatusEmprestimo, status_id, "Status")
    status_registro.status = dados.status
    return save_record(db, status_registro)


@app.delete("/status-emprestimos/{status_id}", status_code=204, tags=["Status de empréstimos"])
def excluir_status(status_id: int, db: Session = Depends(get_db)) -> None:
    delete_record(db, get_record(db, StatusEmprestimo, status_id, "Status"))


@app.get("/emprestimos", response_model=list[EmprestimoOutput], tags=["Empréstimos"])
def listar_emprestimos(db: Session = Depends(get_db)) -> list[Emprestimo]:
    return db.query(Emprestimo).all()


@app.post("/emprestimos", response_model=EmprestimoOutput, status_code=201, tags=["Empréstimos"])
def criar_emprestimo(dados: EmprestimoInput, db: Session = Depends(get_db)) -> Emprestimo:
    return save_record(db, Emprestimo(**dados.model_dump()))


@app.get("/emprestimos/{emprestimo_id}", response_model=EmprestimoOutput, tags=["Empréstimos"])
def buscar_emprestimo(emprestimo_id: int, db: Session = Depends(get_db)) -> Emprestimo:
    return get_record(db, Emprestimo, emprestimo_id, "Empréstimo")


@app.put("/emprestimos/{emprestimo_id}", response_model=EmprestimoOutput, tags=["Empréstimos"])
def atualizar_emprestimo(emprestimo_id: int, dados: EmprestimoInput, db: Session = Depends(get_db)) -> Emprestimo:
    emprestimo = get_record(db, Emprestimo, emprestimo_id, "Empréstimo")
    for campo, valor in dados.model_dump().items():
        setattr(emprestimo, campo, valor)
    return save_record(db, emprestimo)


@app.delete("/emprestimos/{emprestimo_id}", status_code=204, tags=["Empréstimos"])
def excluir_emprestimo(emprestimo_id: int, db: Session = Depends(get_db)) -> None:
    delete_record(db, get_record(db, Emprestimo, emprestimo_id, "Empréstimo"))


@app.get("/livros", response_model=list[LivroOutput], tags=["Livros"])
def listar_livros(db: Session = Depends(get_db)) -> list[Livro]:
    return db.query(Livro).all()


@app.post("/livros", response_model=LivroOutput, status_code=201, tags=["Livros"])
def criar_livro(dados: LivroInput, db: Session = Depends(get_db)) -> Livro:
    return save_record(db, Livro(**dados.model_dump()))


@app.get("/livros/disponiveis", response_model=list[LivroOutput], tags=["Livros"])
def listar_livros_disponiveis(db: Session = Depends(get_db)) -> list[Livro]:
    return db.query(Livro).filter(~Livro.emprestimos.any(emprestimo_em_aberto())).all()


@app.get("/livros/emprestados", response_model=list[LivroOutput], tags=["Livros"])
def listar_livros_emprestados(db: Session = Depends(get_db)) -> list[Livro]:
    return db.query(Livro).filter(Livro.emprestimos.any(emprestimo_em_aberto())).all()


@app.get("/livros/sql/disponiveis", response_model=list[LivroOutput], tags=["Livros"])
def listar_livros_disponiveis_sql(db: Session = Depends(get_db)) -> list[Livro]:
    consulta = text("""
        SELECT livro.*
        FROM livro
        WHERE NOT EXISTS (
            SELECT 1
            FROM emprestimo
            JOIN status_emprestimo ON status_emprestimo.id = emprestimo.status_id
            WHERE emprestimo.livro_id = livro.id
              AND lower(trim(status_emprestimo.status)) IN ('aberto', 'em aberto')
        )
    """)
    return db.query(Livro).from_statement(consulta).all()


@app.get("/livros/sql/emprestados", response_model=list[LivroOutput], tags=["Livros"])
def listar_livros_emprestados_sql(db: Session = Depends(get_db)) -> list[Livro]:
    consulta = text("""
        SELECT livro.*
        FROM livro
        WHERE EXISTS (
            SELECT 1
            FROM emprestimo
            JOIN status_emprestimo ON status_emprestimo.id = emprestimo.status_id
            WHERE emprestimo.livro_id = livro.id
              AND lower(trim(status_emprestimo.status)) IN ('aberto', 'em aberto')
        )
    """)
    return db.query(Livro).from_statement(consulta).all()


@app.get("/livros/{livro_id}", response_model=LivroOutput, tags=["Livros"])
def buscar_livro(livro_id: int, db: Session = Depends(get_db)) -> Livro:
    return get_record(db, Livro, livro_id, "Livro")


@app.put("/livros/{livro_id}", response_model=LivroOutput, tags=["Livros"])
def atualizar_livro(livro_id: int, dados: LivroInput, db: Session = Depends(get_db)) -> Livro:
    livro = get_record(db, Livro, livro_id, "Livro")
    for campo, valor in dados.model_dump().items():
        setattr(livro, campo, valor)
    return save_record(db, livro)


@app.delete("/livros/{livro_id}", status_code=204, tags=["Livros"])
def excluir_livro(livro_id: int, db: Session = Depends(get_db)) -> None:
    delete_record(db, get_record(db, Livro, livro_id, "Livro"))

