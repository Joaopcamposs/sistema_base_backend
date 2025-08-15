from dataclasses import dataclass
from uuid import UUID
from decimal import Decimal

from libs.barramento_de_mensagens.base.barramento import Comando


@dataclass
class CadastrarServico(Comando):
    nome: str
    codigo: str
    descricao: str
    valor: Decimal


@dataclass
class AtualizarServico(Comando):
    nome: str
    codigo: str
    descricao: str
    valor: Decimal
    # campos de busca
    id: UUID | None = None
    codigo_busca: str | None = None


@dataclass
class RemoverServico(Comando):
    id: UUID | None = None
    codigo: str | None = None
