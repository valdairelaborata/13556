
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker

from model import Base, Cliente
from produto_model import Base, Produto


DATABASE_URL = "sqlite:///database.db"  

engine = create_engine(DATABASE_URL)

Base.metadata.create_all(engine)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db = SessionLocal()

# novo_cliente = Cliente(nome="João Silva", email="jvvtgmail.com")
# db.add(novo_cliente)
# db.commit()

# clientes = db.query(Cliente).all()    

# cliente = db.query(Cliente).
# filter(Cliente.nome == "João Silva").first()

# cliente = db.query(Cliente).filter(Cliente.id == 1).first()

# cliente.nome = "João Silva Atualizado"
# cliente.email = "joao.silva.atualizado@gmail.com"

cliente = db.query(Cliente).filter(Cliente.id == 1).first()

db.delete(cliente)
db.commit() 


# novo_produto = Produto(nome="Produto A", preco=10.99)
# db.add(novo_produto)
# db.commit()

db.close()

