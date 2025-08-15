from dataclasses import dataclass
from uuid import UUID

from libs.barramento_de_mensagens.base.barramento import Evento


@dataclass
class ServicoCriado(Evento):
    id: UUID


@dataclass
class ServicoAtualizado(Evento):
    id: UUID


@dataclass
class ServicoRemovido(Evento):
    id: UUID
