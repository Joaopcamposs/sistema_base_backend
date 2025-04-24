from dataclasses import dataclass
from uuid import UUID

from libs.ddd.barramento import Comando


@dataclass
class CadastrarEmpresa(Comando):
    razao_social: str
    nome_responsavel: str
    cnpj: str
    ativo: bool
    nome_fantasia: str | None = None
    email: str | None = None
    cpf: str | None = None


@dataclass
class AtualizarEmpresa(Comando):
    nome_fantasia: str
    nome_responsavel: str
    email: str
    ativo: bool
    razao_social: str | None = None
    cpf: str | None = None
    cnpj: str | None = None
    # campos de busca
    id: UUID | None = None


@dataclass
class RemoverEmpresa(Comando):
    id: UUID | None = None
