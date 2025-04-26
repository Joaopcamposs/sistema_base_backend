from dataclasses import dataclass

from barramento_de_mensagens.base.barramento import Evento


@dataclass(kw_only=True)
class EventoTeste(Evento):
    mensagem: str


@dataclass(kw_only=True)
class EventoTesteAssincrono(Evento):
    mensagem: str
    executar_de_forma_assincrona: bool = True
