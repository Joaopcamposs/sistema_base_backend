from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, UUID4


class CadastrarRegistroDeServicoSchema(BaseModel):
    codigo_sessao_de_servicos: int
    codigo_servico: str
    valor: Decimal
    data_realizacao: datetime


class AtualizarRegistroDeServicoSchema(BaseModel):
    codigo: str
    nome: str
    valor: Decimal
    descricao: str
    data_realizacao: datetime


class LerRegistroDeServicoSchema(BaseModel):
    id: UUID4
    codigo_sessao_de_servicos: int
    codigo_servico: str
    nome: str
    valor: Decimal
    descricao: str
    data_realizacao: datetime
