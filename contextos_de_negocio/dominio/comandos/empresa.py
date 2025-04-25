from dataclasses import dataclass
from uuid import UUID

from libs.ddd.barramento import Comando


@dataclass
class CadastrarEmpresa(Comando):
    razao_social: str
    nome_responsavel: str
    ativo: bool
    cpf: str
    email: str
    cnpj: str | None = None
    nome_fantasia: str | None = None
    id: UUID | None = None


@dataclass
class AtualizarEmpresa(Comando):
    nome_responsavel: str
    email: str
    ativo: bool
    razao_social: str
    cpf: str
    nome_fantasia: str | None = None
    cnpj: str | None = None
    # campos de busca
    id: UUID | None = None
    email_antigo: str | None = None


@dataclass
class RemoverEmpresa(Comando):
    id: UUID | None = None
    email: str | None = None
