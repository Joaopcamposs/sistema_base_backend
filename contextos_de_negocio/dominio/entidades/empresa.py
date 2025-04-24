from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from libs.ddd.dominio.agregado import CamposBase


@dataclass(kw_only=True)
class EmpresaEntidade(CamposBase):
    id: UUID
    razao_social: str | None = None
    nome_fantasia: str
    nome_responsavel: str
    email: str | None = None
    cpf: str | None = None
    cnpj: str
    ativo: bool
