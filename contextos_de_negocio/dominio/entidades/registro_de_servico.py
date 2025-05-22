from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from decimal import Decimal


@dataclass(kw_only=True)
class RegistroDeServicoEntidade:
    id: UUID
    codigo_sessao_de_servicos: int
    codigo_servico: str
    nome: str
    valor: Decimal
    descricao: str
    data_realizacao: datetime
