from __future__ import annotations

from pydantic import BaseModel, UUID4

from contextos_de_negocio.dominio.entidades.cliente import Endereco


class CadastrarClienteSchema(BaseModel):
    nome: str
    cpf: str
    telefone: str
    telefone_2: str
    email: str
    endereco: Endereco


class AtualizarClienteSchema(BaseModel):
    nome: str
    cpf: str
    telefone: str
    telefone_2: str
    email: str
    endereco: Endereco


class LerClienteSchema(BaseModel):
    id: UUID4
    nome: str
    cpf: str
    telefone: str
    telefone_2: str
    email: str
    endereco: Endereco
