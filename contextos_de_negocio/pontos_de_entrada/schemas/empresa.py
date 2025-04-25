from __future__ import annotations

from pydantic import BaseModel, UUID4


class CadastrarEmpresaSchema(BaseModel):
    razao_social: str
    nome_fantasia: str | None = None
    nome_responsavel: str
    email: str
    senha: str
    cpf: str | None = None
    cnpj: str | None = None
    ativo: bool
    deve_criar_usuario: bool = False
    chave_secreta: str | None = None


class AtualizarEmpresaSchema(BaseModel):
    razao_social: str
    nome_fantasia: str | None = None
    nome_responsavel: str
    email: str
    cpf: str | None = None
    cnpj: str | None = None
    ativo: bool


class LerEmpresaSchema(BaseModel):
    id: UUID4
    razao_social: str | None = None
    nome_fantasia: str
    nome_responsavel: str
    email: str
    cpf: str | None = None
    cnpj: str | None = None
    ativo: bool
