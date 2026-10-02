from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base, Cliente, Emprestimo, EnderecoCliente, Livro, Status
from pydantic import BaseModel
 
SQLALCHEMY_DATABASE_URL = 'sqlite:///database.db'
 
engine = create_engine(SQLALCHEMY_DATABASE_URL)
 
Base.metadata.create_all(engine)
 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
 
app = FastAPI()
 
class ClienteView(BaseModel):
    nome: str
    email: str
    endereco_id: int
 
class EnderecoView(BaseModel):
    rua: str
    numero: str
 
class EmprestimoView(BaseModel):
    cliente_id: int
    livro_id: int
    status_id: int
 
class LivroView(BaseModel):
    nome_livro: str
    preco: int
    descricao: str
    categoria: str
 
class StatusView(BaseModel):
    status: str
 
@app.get("/cliente")
def clientes():
    db = SessionLocal()
    clientes = db.query(Cliente).all()
    db.close()
    return {"clientes": clientes}
 
@app.get("/cliente/{cliente_id}")
def cliente(cliente_id: int):
    db = SessionLocal()
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    db.close()
    return {"cliente": cliente}
 
@app.put("/cliente/{cliente_id}")
def cliente(cliente_id: int, dados: ClienteView):
    db = SessionLocal()
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    cliente.nome = dados.nome
    cliente.email = dados.email
    db.commit()
    db.close()
    return {"Alterar": "cliente alterado com sucesso"}
 
@app.post("/cliente")
def cliente(dados:ClienteView):
    db = SessionLocal()
    novo_cliente = Cliente(nome=dados.nome, email=dados.email, endereco_id=dados.endereco_id)
    db.add(novo_cliente)
    db.commit()
    db.close()
    return {"criar": "cliente criado"}
 
@app.delete("/cliente")
def cliente(id: str):
    db = SessionLocal()
    cliente = db.query(Cliente).filter(Cliente.id == id).first()
    db.delete(cliente)
    db.commit()
    db.close()
    return {"excluir_cliente": "Cliente excluído com sucesso"}
 
@app.get("/enderecos")
def endereco():
    db = SessionLocal()
    enderecos = db.query(EnderecoCliente).all()
    db.close()
    return {"enderecos": enderecos}
 
@app.get("/enderecos/{endereco_id}")
def endereco(endereco_id: int):
    db = SessionLocal()
    endereco = db.query(EnderecoCliente).filter(EnderecoCliente.id == endereco_id).first()
    db.close()
    return {"endereco": endereco}
   
@app.post("/enderecos")
def endereco(dados: EnderecoView):
    db = SessionLocal()
    novo_endereco = EnderecoCliente(rua=dados.rua, numero=dados.numero)
    db.add(novo_endereco)
    db.commit()
    db.close()
    return {'Novo endereco': 'Endereco criado'}
 
@app.put("/enderecos/{endereco_id}")
def endereco(endereco_id: int, dados: EnderecoView):
    db = SessionLocal()
    endereco = db.query(EnderecoCliente).filter(EnderecoCliente.id == endereco_id).first()
    endereco.rua = dados.rua
    endereco.numero = dados.numero
    db.commit()
    db.close()
    return {"Alterar": "endereco alterado"}
 
@app.delete("/enderecos/{endereco_id}")
def endereco(endereco_id: int):
    db = SessionLocal()
    endereco = db.query(EnderecoCliente).filter(EnderecoCliente.id == endereco_id).first()
    db.delete(endereco)
    db.commit()
    db.close()
    return {"excluir_endereco": "Endereco excluído"}
 
@app.get("/livros")
def livro():
    db = SessionLocal()
    livros = db.query(Livro).all()
    db.close()
    return {"livros": livros}
 
@app.get("/livros/disponiveis")
def disponiveis():
    db = SessionLocal()
    livros = db.query(Livro).all()
    livros_disponiveis = livros
    emprestimos = db.query(Emprestimo).where(Emprestimo.status_id == 2).all()
 
    for livro in livros:
        for emprestimo in emprestimos:
            if emprestimo.livro_id == livro.id:
                livros_disponiveis.remove(livro)
       
    return livros_disponiveis
 
@app.get("/livros/emprestado")
def emprestados():
    db = SessionLocal()
    livros_emprestado = []
    emprestimos = db.query(Emprestimo).where(Emprestimo.status_id == 2).all()
 
    for emprestimo in emprestimos:
        livros_emprestado.append(emprestimo.livro)
 
    return livros_emprestado
 
@app.get("/livros/{livro_id}")
def livro(livro_id: int):
    db = SessionLocal()
    livro = db.query(Livro).filter(Livro.id == livro_id).first()
    db.close()
    return {"livro": livro}
 
@app.get("/livros/categoria/{categoria}")
def livros_por_categoria(categoria: str):
    db = SessionLocal()
    livros = db.query(Livro).filter(Livro.categoria == categoria).all()
    db.close()
    return {"livros": livros}
 
@app.post("/livros")
def livro(dados: LivroView):
    db = SessionLocal()
    novo_livro = Livro(nome_livro=dados.nome_livro, preco=dados.preco, descricao=dados.descricao, categoria=dados.categoria)
    db.add(novo_livro)
    db.commit()
    db.close()
    return {'Novo livro': 'Livro criado'}
 
@app.put("/livros/{livro_id}")
def livro(livro_id: int, dados: LivroView):
    db = SessionLocal()
    livro = db.query(Livro).filter(Livro.id == livro_id).first()
    livro.nome_livro = dados.nome_livro
    livro.preco = dados.preco
    livro.descricao = dados.descricao
    livro.categoria = dados.categoria
    db.commit()
    db.close()
    return {"Alterar": "livro alterado"}
 
@app.delete("/livros/{livro_id}")
def livro(livro_id: int):
    db = SessionLocal()
    livro = db.query(Livro).filter(Livro.id == livro_id).first()
    db.delete(livro)
    db.commit()
    db.close()
    return {"excluir_livro": "Livro excluído"}
 
@app.get("/emprestimos")
def emprestimo():
    db = SessionLocal()
    emprestimos = db.query(Emprestimo).all()
    db.close()
    return {"emprestimos": emprestimos}
 
@app.get("/emprestimos/{emprestimo_id}")  
def emprestimo(emprestimo_id: int):
    db = SessionLocal()
    emprestimo = db.query(Emprestimo).filter(Emprestimo.id == emprestimo_id).first()
    db.close()
    return {"emprestimo": emprestimo}
   
@app.post("/emprestimos")
def emprestimo(dados: EmprestimoView):
    db = SessionLocal()
    novo_emprestimo = Emprestimo(cliente_id=dados.cliente_id, livro_id=dados.livro_id, status_id=dados.status_id)
    db.add(novo_emprestimo)
    db.commit()
    db.close()
    return {'Novo emprestimo': 'Emprestimo criado'}
 
@app.put("/emprestimos/{emprestimo_id}")
def emprestimo(emprestimo_id: int, dados: EmprestimoView):
    db = SessionLocal()
    emprestimo = db.query(Emprestimo).filter(Emprestimo.id == emprestimo_id).first()
    emprestimo.cliente_id = dados.cliente_id
    emprestimo.livro_id = dados.livro_id
    emprestimo.status_id = dados.status_id
    db.commit()
    db.close()
    return {"Alterar": "emprestimo alterado"}
 
@app.get("/status")
def status():
    db = SessionLocal()
    status = db.query(Status).all()
    db.close()
    return {"status": status}
 
@app.get("/status/{status_id}")
def status(status_id: int):
    db = SessionLocal()
    statu = db.query(Status).filter(Status.id == status_id).first()
    db.close()
    return {"status": statu}