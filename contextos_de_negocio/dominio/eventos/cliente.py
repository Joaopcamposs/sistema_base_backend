from dataclasses import dataclass
from uuid import UUID

from libs.barramento_de_mensagens.base.barramento import Evento


@dataclass
class ClienteCriado(Evento):
    id: UUID


@dataclass
class ClienteAtualizado(Evento):
    id: UUID


@dataclass
class ClienteRemovido(Evento):
    id: UUID
