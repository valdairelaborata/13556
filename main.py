from fastapi import FastAPI
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker

from model import Base, Cliente
from produto_model import Base, Produto


DATABASE_URL = "sqlite:///database.db"  

engine = create_engine(DATABASE_URL)

Base.metadata.create_all(engine)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


app = FastAPI() 



@app.get("/clientes")
def lista_clientes():
    db = SessionLocal()
    clientes = db.query(Cliente).all()
    db.close()
    return {"clientes": clientes}


@app.get("/clientes/{cliente_id}")
def busca_cliente(cliente_id: str):
    return {"cliente": f"cliente {cliente_id} encontrado"}  


@app.put("/clientes")
def alterar_cliente():
    return {"alterar": "cliente alterado"}

@app.delete("/clientes")
def exluir_cliente():
    return {"excluir": "cliente excluido"}

@app.post("/clientes")
def criar_cliente():
    return {"criar": "cliente criado"}

