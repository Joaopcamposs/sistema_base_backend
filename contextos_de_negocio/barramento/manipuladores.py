from barramento_de_mensagens.manipuladores import (
    ManipuladoresDeEventos,
    ManipuladoresDeComandos,
)

from contextos_de_negocio.dominio.comandos.cliente import (
    CadastrarCliente,
    AtualizarCliente,
    RemoverCliente,
)
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
from contextos_de_negocio.dominio.eventos.cliente import (
    ClienteCriado,
    ClienteAtualizado,
    ClienteRemovido,
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
    ChegouAHoraDeCriarUsuarioADMDaEmpresa,
)
from contextos_de_negocio.servicos.executores.cliente import (
    cadastrar_cliente,
    atualizar_cliente,
    remover_cliente,
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
    atualizar_usuario_publico,
    remover_usuario_publico,
)

EVENT_HANDLERS: ManipuladoresDeEventos = ManipuladoresDeEventos(
    {
        EventoTeste: [evento_teste],
        EventoTesteAssincrono: [evento_teste_assincrono],
        # usuario
        UsuarioCriado: [cadastrar_usuario_publico],
        UsuarioAtualizado: [atualizar_usuario_publico],
        UsuarioRemovido: [remover_usuario_publico],
        # empresa
        EmpresaCriada: [],
        EmpresaAtualizada: [],
        EmpresaRemovida: [],
        ChegouAHoraDeCriarUsuarioInicialDaEmpresa: [cadastrar_usuario],
        ChegouAHoraDeCriarUsuarioADMDaEmpresa: [cadastrar_usuario],
        # cliente
        ClienteCriado: [],
        ClienteAtualizado: [],
        ClienteRemovido: [],
    }
)

COMMAND_HANDLERS: ManipuladoresDeComandos = ManipuladoresDeComandos(
    {
        ComandoTeste: comando_teste,
        CadastrarUsuario: cadastrar_usuario,
        AtualizarUsuario: atualizar_usuario,
        RemoverUsuario: remover_usuario,
        CadastrarEmpresa: cadastrar_empresa,
        AtualizarEmpresa: atualizar_empresa,
        RemoverEmpresa: remover_empresa,
        CadastrarCliente: cadastrar_cliente,
        AtualizarCliente: atualizar_cliente,
        RemoverCliente: remover_cliente,
    }
)
