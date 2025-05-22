from dataclasses import dataclass
from uuid import UUID
from decimal import Decimal


@dataclass(kw_only=True)
class ServicoEntidade:
    id: UUID
    codigo: str
    nome: str
    descricao: str
    valor: Decimal
