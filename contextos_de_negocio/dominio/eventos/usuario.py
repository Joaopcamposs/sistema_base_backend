from dataclasses import dataclass, field
from uuid import UUID

from pydantic import UUID4

from libs.ddd.barramento import Evento


@dataclass
class UsuarioCriado(Evento):
    id: UUID


@dataclass
class UsuarioAtualizado(Evento):
    id: UUID


@dataclass
class UsuarioRemovido(Evento):
    id: UUID


@dataclass
class ChegouAHoraDeCriarUsuarioInicialDaEmpresa(Evento):
    empresa: UUID4
    nome: str
    email: str
    cpf: str
    senha: str
    ativo: bool
    adm: bool
    permissoes: list[str] = field(default_factory=list)
