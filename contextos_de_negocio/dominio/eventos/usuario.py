from dataclasses import dataclass
from uuid import UUID

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
