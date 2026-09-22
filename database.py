import os
from pathlib import Path

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import declarative_base, sessionmaker


database_path = Path(os.environ.get("DATABASE_PATH", "instance/clientes.sqlite3"))
database_path.parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(
    f"sqlite:///{database_path.as_posix()}",
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


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
