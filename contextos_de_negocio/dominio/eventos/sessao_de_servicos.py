from dataclasses import dataclass
from uuid import UUID

from libs.barramento_de_mensagens.base.barramento import Evento


@dataclass
class SessaoDeServicosCriado(Evento):
    id: UUID


@dataclass
class SessaoDeServicosAtualizado(Evento):
    id: UUID


@dataclass
class SessaoDeServicosRemovido(Evento):
    id: UUID
