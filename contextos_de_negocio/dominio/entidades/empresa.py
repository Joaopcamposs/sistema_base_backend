from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from libs.ddd.dominio.agregado import CamposBase
from libs.utils.tipos_basicos import Email, CPF, CNPJ


@dataclass(kw_only=True)
class EmpresaEntidade(CamposBase):
    id: UUID
    razao_social: str
    nome_fantasia: str | None = None
    nome_responsavel: str
    email: Email
    cpf: CPF
    cnpj: CNPJ | None = None
    ativo: bool
