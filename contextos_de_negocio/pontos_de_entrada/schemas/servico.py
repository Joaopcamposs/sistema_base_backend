from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel, UUID4


class CadastrarServicoSchema(BaseModel):
    nome: str
    codigo: str
    descricao: str
    valor: Decimal


class AtualizarServicoSchema(BaseModel):
    nome: str
    codigo: str
    descricao: str
    valor: Decimal


class LerServicoSchema(BaseModel):
    id: UUID4
    nome: str
    codigo: str
    descricao: str
    valor: Decimal
