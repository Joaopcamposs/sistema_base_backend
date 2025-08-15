from dataclasses import dataclass
from uuid import UUID

from libs.barramento_de_mensagens.base.barramento import Evento


@dataclass
class RegistroDeServicoCriado(Evento):
    id: UUID


@dataclass
class RegistroDeServicoAtualizado(Evento):
    id: UUID


@dataclass
class RegistroDeServicoRemovido(Evento):
    id: UUID
