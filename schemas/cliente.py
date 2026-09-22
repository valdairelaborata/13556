from pydantic import BaseModel, ConfigDict, EmailStr, Field


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
