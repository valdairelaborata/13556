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
    db = SessionLocal()
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    db.close()
    return {"cliente": cliente}  


@app.put("/clientes/{cliente_id}")
def alterar_cliente(cliente_id: str):
    db = SessionLocal()
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    cliente.nome = "João Silva Atualizado"
    db.commit()
    db.close()
    return {"alterar": "cliente alterado"}

@app.delete("/clientes")
def exluir_cliente():
    return {"excluir": "cliente excluido"}

@app.post("/clientes")
def criar_cliente():
    return {"criar": "cliente criado"}

 