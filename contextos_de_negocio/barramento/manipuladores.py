from contextos_de_negocio.dominio.comandos.empresa import (
    CadastrarEmpresa,
    AtualizarEmpresa,
    RemoverEmpresa,
)
from contextos_de_negocio.dominio.comandos.teste import ComandoTeste
from contextos_de_negocio.dominio.comandos.usuario import (
    CadastrarUsuario,
    AtualizarUsuario,
    RemoverUsuario,
)
from contextos_de_negocio.dominio.eventos.empresa import (
    EmpresaCriada,
    EmpresaAtualizada,
    EmpresaRemovida,
)
from contextos_de_negocio.dominio.eventos.teste import EventoTeste, EventoTesteAssincrono
from contextos_de_negocio.dominio.eventos.usuario import (
    UsuarioCriado,
    UsuarioAtualizado,
    UsuarioRemovido,
    ChegouAHoraDeCriarUsuarioInicialDaEmpresa,
)
from contextos_de_negocio.servicos.executores.empresa import (
    cadastrar_empresa,
    atualizar_empresa,
    remover_empresa,
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
    cadastrar_usuario_publico,
)
from libs.ddd.barramento import Evento, Comando

EVENT_HANDLERS: dict[type[Evento], list[callable]] = {
    EventoTeste: [evento_teste],
    EventoTesteAssincrono: [evento_teste_assincrono],
    UsuarioCriado: [cadastrar_usuario_publico],
    UsuarioAtualizado: [],
    UsuarioRemovido: [],
    EmpresaCriada: [],
    EmpresaAtualizada: [],
    EmpresaRemovida: [],
    ChegouAHoraDeCriarUsuarioInicialDaEmpresa: [cadastrar_usuario],
}

COMMAND_HANDLERS: dict[type[Comando], callable] = {
    ComandoTeste: comando_teste,
    CadastrarUsuario: cadastrar_usuario,
    AtualizarUsuario: atualizar_usuario,
    RemoverUsuario: remover_usuario,
    CadastrarEmpresa: cadastrar_empresa,
    AtualizarEmpresa: atualizar_empresa,
    RemoverEmpresa: remover_empresa,
}
