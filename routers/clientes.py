from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from database import get_db
from models import Cliente, Endereco
from schemas import ClienteResponse, ClienteSchema

router = APIRouter(prefix="/api/clientes", tags=["clientes"])


def buscar_cliente(session: Session, cliente_id: int):
    return (
        session.query(Cliente)
        .options(selectinload(Cliente.enderecos))
        .filter(Cliente.id == cliente_id)
        .first()
    )


def montar_cliente(dados: ClienteSchema):
    return Cliente(
        nome=dados.nome,
        email=str(dados.email),
        telefone=dados.telefone,
        enderecos=[
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
        ],
    )


def atualizar_enderecos(cliente: Cliente, dados: ClienteSchema):
    cliente.enderecos = [
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


@router.get("", response_model=list[ClienteResponse])
def listar_clientes(session: Session = Depends(get_db)):
    return (
        session.query(Cliente)
        .options(selectinload(Cliente.enderecos))
        .order_by(Cliente.nome)
        .all()
    )


@router.get("/{cliente_id}", response_model=ClienteResponse)
def obter_cliente(cliente_id: int, session: Session = Depends(get_db)):
    cliente = buscar_cliente(session, cliente_id)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente


@router.post("", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
def criar_cliente(dados: ClienteSchema, session: Session = Depends(get_db)):
    cliente = montar_cliente(dados)
    session.add(cliente)
    try:
        session.commit()
    except IntegrityError as error:
        session.rollback()
        raise HTTPException(status_code=409, detail="Já existe um cliente com este e-mail") from error
    session.refresh(cliente)
    return buscar_cliente(session, cliente.id)


@router.put("/{cliente_id}", response_model=ClienteResponse)
def atualizar_cliente(cliente_id: int, dados: ClienteSchema, session: Session = Depends(get_db)):
    cliente = buscar_cliente(session, cliente_id)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    cliente.nome = dados.nome
    cliente.email = str(dados.email)
    cliente.telefone = dados.telefone
    atualizar_enderecos(cliente, dados)
    try:
        session.commit()
    except IntegrityError as error:
        session.rollback()
        raise HTTPException(status_code=409, detail="Já existe outro cliente com este e-mail") from error
    return buscar_cliente(session, cliente_id)


@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_cliente(cliente_id: int, session: Session = Depends(get_db)):
    cliente = buscar_cliente(session, cliente_id)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    session.delete(cliente)
    session.commit()
