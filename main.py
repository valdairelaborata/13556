from fastapi import FastAPI
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel, ConfigDict


# from produto_model import Base, Produto
from model import Base, Cliente, Endereco


DATABASE_URL = "sqlite:///database.db"  

engine = create_engine(DATABASE_URL)

Base.metadata.create_all(engine)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


app = FastAPI() 

class ClienteViewBase(BaseModel):    
    nome: str
    email: str
    

class ClienteViewInclude(ClienteViewBase):    
    endereco_id: int

class ClienteViewGet(ClienteViewBase):       
    endereco: str


class ClienteResponse(BaseModel):
    cliente: ClienteViewGet


class EnderecoView(BaseModel):
    rua: str
    numero: str


@app.get("/clientes")
def lista_clientes():
    db = SessionLocal()
    clientes = db.query(Cliente).all()
    db.close()
    return {"clientes": clientes}


@app.get("/clientes/{cliente_id}", response_model=ClienteResponse)
def busca_cliente(cliente_id: str):
    db = SessionLocal()
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        db.close()
        return {"cliente": None}

    cliente_view = ClienteViewGet(
        nome=cliente.nome,
        email=cliente.email,
        endereco=cliente.endereco.rua + ", " + cliente.endereco.numero,
    )
    db.close()


    return {"cliente": cliente_view}  


@app.put("/clientes/{cliente_id}")
def alterar_cliente(cliente_id: str, dados: ClienteViewInclude):
    db = SessionLocal()
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    cliente.nome = dados.nome
    cliente.email = dados.email
    db.commit()
    db.close()
    return {"alterar": "cliente alterado"}

@app.delete("/clientes/{cliente_id}")
def exluir_cliente(cliente_id: str):
    db = SessionLocal()
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    db.delete(cliente)
    db.commit()
    db.close()
    return {"excluir": "cliente excluido"}

@app.post("/clientes")
def criar_cliente(dados: ClienteViewInclude):
    db = SessionLocal()
    endereco = db.query(Endereco).filter(Endereco.id == dados.endereco_id).first()  
    if not endereco:
        db.close()
        return {"error": "Endereço não encontrado"}
    
    novo_cliente = Cliente(nome=dados.nome, email=dados.email, endereco_id=dados.endereco_id)
    db.add(novo_cliente)
    db.commit()
    db.close()
    return {"criar": "cliente criado"}


@app.post("/enderecos")
def criar_endereco(endereco: EnderecoView):
    db = SessionLocal()
    novo_endereco = Endereco(rua=endereco.rua, numero=endereco.numero)
    db.add(novo_endereco)
    db.commit()
    db.close()
    return {"criar": "endereco criado"}


@app.get("/enderecos/{id}")
def buscar_endereco(id: int):
    db = SessionLocal()
    endereco = db.query(Endereco).filter(Endereco.id == id).first()
    db.close()
    return {"endereco": endereco}