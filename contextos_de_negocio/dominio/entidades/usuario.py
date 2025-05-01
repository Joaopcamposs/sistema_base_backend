from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from libs.ddd.dominio.agregado import CamposBase, SegurancaDoUsuario
from libs.utils.tipos_basicos import Email, CPF


@dataclass(kw_only=True)
class UsuarioEntidade(CamposBase, SegurancaDoUsuario):
    id: UUID
    empresa: UUID
    nome: str
    email: Email
    cpf: CPF
    ativo: bool
    adm: bool
    permissoes: list[str] = field(default_factory=list)

    _senha_hash: str


@dataclass(kw_only=True)
class UsuarioPublicoEntidade(CamposBase, SegurancaDoUsuario):
    id: UUID
    empresa: UUID
    ativo: bool
    email_criptografado: bytes
    email_hash: str
    _senha_hash: str
