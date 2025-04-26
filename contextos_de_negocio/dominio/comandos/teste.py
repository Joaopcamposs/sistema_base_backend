from dataclasses import dataclass

from barramento_de_mensagens.base.barramento import Comando


@dataclass
class ComandoTeste(Comando):
    mensagem: str
