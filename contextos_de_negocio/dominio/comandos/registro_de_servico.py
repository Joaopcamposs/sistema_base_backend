from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from decimal import Decimal

from barramento_de_mensagens.base.barramento import Comando


@dataclass
class CadastrarRegistroDeServico(Comando):
    codigo_sessao_de_servicos: int
    codigo_servico: str
    valor: Decimal
    data_realizacao: datetime


@dataclass
class AtualizarRegistroDeServico(Comando):
    codigo: str
    nome: str
    valor: Decimal
    descricao: str
    data_realizacao: datetime
    # campos de busca
    id: UUID | None = None


@dataclass
class RemoverRegistroDeServico(Comando):
    id: UUID | None = None
