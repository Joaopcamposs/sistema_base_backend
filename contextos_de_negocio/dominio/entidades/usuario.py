from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from libs.ddd.dominio.agregado import CamposBase
from libs.utils.constantes import pwd_context


@dataclass(kw_only=True)
class UsuarioEntidade(CamposBase):
    id: UUID
    empresa: UUID
    nome: str
    email: str
    cpf: str
    ativo: bool
    adm: bool
    permissoes: list[str] = field(default_factory=list)

    _senha: str

    def verificar_senha(self, senha: str) -> bool:
        senhas_conferem = pwd_context.verify(secret=senha, hash=self._senha)
        return senhas_conferem
