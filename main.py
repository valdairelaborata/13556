import os
from pathlib import Path

from fastapi import FastAPI, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr
from sqlalchemy import ForeignKey, String, create_engine, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship, selectinload, sessionmaker

app = FastAPI(title="Cadastro de clientes")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
database_path = Path(os.environ.get("DATABASE_PATH", "instance/clientes.sqlite3"))
database_path.parent.mkdir(parents=True, exist_ok=True)
engine = create_engine(f"sqlite:///{database_path.as_posix()}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class Client(Base):
    __tablename__ = "clientes"
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    telefone: Mapped[str] = mapped_column(String(40), default="")
    endereco: Mapped["Address"] = relationship(back_populates="cliente", cascade="all, delete-orphan", uselist=False)


class Address(Base):
    __tablename__ = "enderecos"
    id: Mapped[int] = mapped_column(primary_key=True)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("clientes.id", ondelete="CASCADE"), unique=True)
    logradouro: Mapped[str] = mapped_column(String(160), nullable=False)
    numero: Mapped[str] = mapped_column(String(20), nullable=False)
    complemento: Mapped[str] = mapped_column(String(80), default="")
    bairro: Mapped[str] = mapped_column(String(100), nullable=False)
    cidade: Mapped[str] = mapped_column(String(100), nullable=False)
    estado: Mapped[str] = mapped_column(String(2), nullable=False)
    cep: Mapped[str] = mapped_column(String(12), nullable=False)
    cliente: Mapped[Client] = relationship(back_populates="endereco")


class ClientPayload(BaseModel):
    nome: str
    email: EmailStr
    telefone: str = ""
    logradouro: str
    numero: str
    complemento: str = ""
    bairro: str
    cidade: str
    estado: str
    cep: str


def serialize_client(client):
    address = client.endereco
    return {
        "id": client.id, "nome": client.nome, "email": client.email, "telefone": client.telefone,
        "logradouro": address.logradouro if address else None, "numero": address.numero if address else None,
        "complemento": address.complemento if address else None, "bairro": address.bairro if address else None,
        "cidade": address.cidade if address else None, "estado": address.estado if address else None,
        "cep": address.cep if address else None,
    }


def client_query(session: Session, client_id=None):
    query = select(Client).options(selectinload(Client.endereco)).order_by(Client.nome)
    if client_id is not None:
        query = query.where(Client.id == client_id)
        return session.scalar(query)
    return list(session.scalars(query))


def save_client(data, client_id=None):
    with SessionLocal() as session:
        if client_id is None:
            client = Client(nome=data.nome, email=str(data.email), telefone=data.telefone)
            client.endereco = Address(
                logradouro=data.logradouro, numero=data.numero, complemento=data.complemento,
                bairro=data.bairro, cidade=data.cidade, estado=data.estado.upper(), cep=data.cep,
            )
            session.add(client)
            session.commit()
            return client.id
        else:
            client = client_query(session, client_id)
            if client is None:
                raise HTTPException(status_code=404, detail="Cliente não encontrado")
            client.nome, client.email, client.telefone = data.nome, str(data.email), data.telefone
            client.endereco.logradouro, client.endereco.numero = data.logradouro, data.numero
            client.endereco.complemento, client.endereco.bairro = data.complemento, data.bairro
            client.endereco.cidade, client.endereco.estado, client.endereco.cep = data.cidade, data.estado.upper(), data.cep
            session.commit()
            return client_id


@app.get("/api/clientes")
def list_clients():
    with SessionLocal() as session:
        return [serialize_client(client) for client in client_query(session)]


@app.get("/api/clientes/{client_id}")
def get_client(client_id: int):
    with SessionLocal() as session:
        client = client_query(session, client_id)
    if client is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return serialize_client(client)


@app.post("/api/clientes", status_code=status.HTTP_201_CREATED)
def create_client(payload: ClientPayload):
    try:
        client_id = save_client(payload)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Já existe um cliente com este e-mail")
    return get_client(client_id)


@app.put("/api/clientes/{client_id}")
def update_client(client_id: int, payload: ClientPayload):
    with SessionLocal() as session:
        if client_query(session, client_id) is None:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
    try:
        save_client(payload, client_id)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Já existe outro cliente com este e-mail")
    return get_client(client_id)


@app.delete("/api/clientes/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(client_id: int):
    with SessionLocal() as session:
        client = client_query(session, client_id)
        if client is None:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        session.delete(client)
        session.commit()


Base.metadata.create_all(engine)


def form_data(nome, email, telefone, logradouro, numero, complemento, bairro, cidade, estado, cep):
    return ClientPayload(
        nome=nome, email=email, telefone=telefone, logradouro=logradouro,
        numero=numero, complemento=complemento, bairro=bairro, cidade=cidade,
        estado=estado.upper(), cep=cep,
    )


@app.get("/", response_class=HTMLResponse)
def index(request: Request, message: str = ""):
    with SessionLocal() as session:
        clients = [serialize_client(client) for client in client_query(session)]
    return templates.TemplateResponse("index.html", {"request": request, "clients": clients, "message": message})


@app.get("/clientes/novo", response_class=HTMLResponse)
def new_client_page(request: Request):
    return templates.TemplateResponse("client_form.html", {"request": request, "client": {}, "page_title": "Novo cliente", "error": ""})


@app.post("/clientes/novo")
def create_client_page(
    request: Request,
    nome: str = Form(...), email: str = Form(...), telefone: str = Form(""),
    logradouro: str = Form(...), numero: str = Form(...), complemento: str = Form(""),
    bairro: str = Form(...), cidade: str = Form(...), estado: str = Form(...), cep: str = Form(...),
):
    try:
        save_client(form_data(nome, email, telefone, logradouro, numero, complemento, bairro, cidade, estado, cep))
    except (IntegrityError, ValueError):
        data = locals()
        return templates.TemplateResponse("client_form.html", {"request": request, "client": data, "page_title": "Novo cliente", "error": "Verifique os dados e confirme que o e-mail ainda não está cadastrado."}, status_code=400)
    return RedirectResponse(url="/?message=Cliente+cadastrado+com+sucesso", status_code=303)


@app.get("/clientes/{client_id}/editar", response_class=HTMLResponse)
def edit_client_page(request: Request, client_id: int):
    with SessionLocal() as session:
        client = client_query(session, client_id)
    if client is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return templates.TemplateResponse("client_form.html", {"request": request, "client": serialize_client(client), "page_title": "Editar cliente", "error": ""})


@app.post("/clientes/{client_id}/editar")
def update_client_page(
    request: Request,
    client_id: int,
    nome: str = Form(...), email: str = Form(...), telefone: str = Form(""),
    logradouro: str = Form(...), numero: str = Form(...), complemento: str = Form(""),
    bairro: str = Form(...), cidade: str = Form(...), estado: str = Form(...), cep: str = Form(...),
):
    try:
        save_client(form_data(nome, email, telefone, logradouro, numero, complemento, bairro, cidade, estado, cep), client_id)
    except (IntegrityError, ValueError):
        data = locals()
        return templates.TemplateResponse("client_form.html", {"request": request, "client": data, "page_title": "Editar cliente", "error": "Verifique os dados e confirme que o e-mail ainda não está cadastrado."}, status_code=400)
    return RedirectResponse(url="/?message=Cliente+atualizado+com+sucesso", status_code=303)


@app.post("/clientes/{client_id}/excluir")
def delete_client_page(client_id: int):
    with SessionLocal() as session:
        client = client_query(session, client_id)
        if client is not None:
            session.delete(client)
            session.commit()
    return RedirectResponse(url="/?message=Cliente+excluido+com+sucesso", status_code=303)