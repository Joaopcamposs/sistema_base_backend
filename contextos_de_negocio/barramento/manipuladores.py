from contextos_de_negocio.dominio.comandos.teste import ComandoTeste
from contextos_de_negocio.dominio.comandos.usuario import (
    CadastrarUsuario,
    AtualizarUsuario,
    RemoverUsuario,
)
from contextos_de_negocio.dominio.eventos.teste import EventoTeste, EventoTesteAssincrono
from contextos_de_negocio.dominio.eventos.usuario import (
    UsuarioCriado,
    UsuarioAtualizado,
    UsuarioRemovido,
)
from contextos_de_negocio.servicos.executores.teste import (
    evento_teste_assincrono,
    evento_teste,
    comando_teste,
)
from contextos_de_negocio.servicos.executores.usuario import (
    remover_usuario,
    atualizar_usuario,
    cadastrar_usuario,
)
from libs.ddd.barramento import Evento, Comando

EVENT_HANDLERS: dict[type[Evento], list[callable]] = {
    EventoTeste: [evento_teste],
    EventoTesteAssincrono: [evento_teste_assincrono],
    UsuarioCriado: [],
    UsuarioAtualizado: [],
    UsuarioRemovido: [],
}

COMMAND_HANDLERS: dict[type[Comando], callable] = {
    ComandoTeste: comando_teste,
    CadastrarUsuario: cadastrar_usuario,
    AtualizarUsuario: atualizar_usuario,
    RemoverUsuario: remover_usuario,
}
