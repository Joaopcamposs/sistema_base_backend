"""
Testes unitários para comandos e eventos do domínio.
"""

from uuid import uuid4

from contextos_de_negocio.dominio.comandos.usuario import (
    CadastrarUsuario,
    AtualizarUsuario,
    RemoverUsuario,
)
from contextos_de_negocio.dominio.comandos.empresa import (
    CadastrarEmpresa,
)
from contextos_de_negocio.dominio.comandos.cliente import (
    CadastrarCliente,
)
from contextos_de_negocio.dominio.eventos.usuario import (
    UsuarioCriado,
    UsuarioAtualizado,
    UsuarioRemovido,
)
from contextos_de_negocio.dominio.eventos.empresa import (
    EmpresaCriada,
    EmpresaAtualizada,
)
from contextos_de_negocio.dominio.eventos.cliente import (
    ClienteCriado,
    ClienteAtualizado,
    ClienteRemovido,
)
from libs.barramento_de_mensagens.base.barramento import Comando, Evento


class TestComandosUsuario:
    """Testes para comandos de usuário."""

    def test_deve_criar_comando_cadastrar_usuario(self):
        """Deve criar comando CadastrarUsuario."""
        empresa_id = uuid4()
        comando = CadastrarUsuario(
            nome="Teste",
            email="teste@teste.com",
            cpf="52998224725",
            senha="senha123",
            ativo=True,
            adm=False,
            empresa=empresa_id,
            permissoes=["leitura"],
        )

        assert comando.nome == "Teste"
        assert comando.email == "teste@teste.com"
        assert comando.empresa == empresa_id
        assert isinstance(comando, Comando)

    def test_deve_criar_comando_atualizar_usuario(self):
        """Deve criar comando AtualizarUsuario."""
        usuario_id = uuid4()
        comando = AtualizarUsuario(
            nome="Teste Atualizado",
            email="atualizado@teste.com",
            cpf="52998224725",
            senha="nova_senha",
            ativo=True,
            adm=True,
            permissoes=["admin"],
            id=usuario_id,
            email_antigo="teste@teste.com",
        )

        assert comando.nome == "Teste Atualizado"
        assert comando.id == usuario_id
        assert comando.email_antigo == "teste@teste.com"
        assert isinstance(comando, Comando)

    def test_deve_criar_comando_remover_usuario(self):
        """Deve criar comando RemoverUsuario."""
        usuario_id = uuid4()
        comando = RemoverUsuario(
            id=usuario_id,
            email="teste@teste.com",
        )

        assert comando.id == usuario_id
        assert comando.email == "teste@teste.com"
        assert isinstance(comando, Comando)

    def test_comando_deve_censurar_senha_no_repr(self):
        """Comando deve censurar campo senha no __repr__."""
        comando = CadastrarUsuario(
            nome="Teste",
            email="teste@teste.com",
            cpf="52998224725",
            senha="senha_secreta_123",
            ativo=True,
            adm=False,
            empresa=uuid4(),
            permissoes=[],
        )

        repr_comando = repr(comando)
        assert "senha_secreta_123" not in repr_comando
        assert "***" in repr_comando


class TestComandosEmpresa:
    """Testes para comandos de empresa."""

    def test_deve_criar_comando_cadastrar_empresa(self):
        """Deve criar comando CadastrarEmpresa."""
        empresa_id = uuid4()
        comando = CadastrarEmpresa(
            razao_social="Empresa Teste LTDA",
            nome_responsavel="João",
            email="empresa@teste.com",
            cpf="52998224725",
            senha="senha123",
            ativo=True,
            id=empresa_id,
        )

        assert comando.razao_social == "Empresa Teste LTDA"
        assert comando.email == "empresa@teste.com"
        assert comando.id == empresa_id
        assert isinstance(comando, Comando)


class TestComandosCliente:
    """Testes para comandos de cliente."""

    def test_deve_criar_comando_cadastrar_cliente(self):
        """Deve criar comando CadastrarCliente."""
        from contextos_de_negocio.dominio.entidades.cliente import Endereco
        from libs.utils.tipos_basicos import CPF, Email

        endereco = Endereco(
            cep="01310100",
            rua="Rua Teste",
            numero="100",
            complemento=None,
            bairro="Centro",
            cidade="São Paulo",
            estado="SP",
            pais="Brasil",
        )
        comando = CadastrarCliente(
            nome="Cliente Teste",
            cpf=CPF("52998224725"),
            telefone="11999999999",
            telefone_2="",
            email=Email("cliente@teste.com"),
            endereco=endereco,
        )

        assert comando.nome == "Cliente Teste"
        assert comando.endereco.cidade == "São Paulo"
        assert isinstance(comando, Comando)


class TestEventosUsuario:
    """Testes para eventos de usuário."""

    def test_deve_criar_evento_usuario_criado(self):
        """Deve criar evento UsuarioCriado."""
        usuario_id = uuid4()
        evento = UsuarioCriado(id=usuario_id)

        assert evento.id == usuario_id
        assert isinstance(evento, Evento)

    def test_deve_criar_evento_usuario_atualizado(self):
        """Deve criar evento UsuarioAtualizado."""
        usuario_id = uuid4()
        evento = UsuarioAtualizado(id=usuario_id)

        assert evento.id == usuario_id
        assert isinstance(evento, Evento)

    def test_deve_criar_evento_usuario_removido(self):
        """Deve criar evento UsuarioRemovido."""
        usuario_id = uuid4()
        evento = UsuarioRemovido(id=usuario_id)

        assert evento.id == usuario_id
        assert isinstance(evento, Evento)

    def test_evento_deve_ter_flag_execucao_assincrona(self):
        """Evento deve ter flag de execução assíncrona."""
        evento = UsuarioCriado(id=uuid4())

        assert hasattr(evento, "executar_de_forma_assincrona")
        assert evento.executar_de_forma_assincrona is False  # padrão

    def test_evento_deve_permitir_execucao_assincrona(self):
        """Evento deve permitir configurar execução assíncrona."""
        evento = UsuarioCriado(
            id=uuid4(),
            executar_de_forma_assincrona=True,
            fila_de_execucao_assincrona="fila_teste",
            prioridade_de_execucao_assincrona=5,
            tempo_de_atraso_para_execucao_assincrona=10,
        )

        assert evento.executar_de_forma_assincrona is True
        assert evento.fila_de_execucao_assincrona == "fila_teste"
        assert evento.prioridade_de_execucao_assincrona == 5
        assert evento.tempo_de_atraso_para_execucao_assincrona == 10


class TestEventosEmpresa:
    """Testes para eventos de empresa."""

    def test_deve_criar_evento_empresa_criada(self):
        """Deve criar evento EmpresaCriada."""
        empresa_id = uuid4()
        evento = EmpresaCriada(id=empresa_id)

        assert evento.id == empresa_id
        assert isinstance(evento, Evento)

    def test_deve_criar_evento_empresa_atualizada(self):
        """Deve criar evento EmpresaAtualizada."""
        empresa_id = uuid4()
        evento = EmpresaAtualizada(id=empresa_id)

        assert evento.id == empresa_id
        assert isinstance(evento, Evento)


class TestEventosCliente:
    """Testes para eventos de cliente."""

    def test_deve_criar_evento_cliente_criado(self):
        """Deve criar evento ClienteCriado."""
        cliente_id = uuid4()
        evento = ClienteCriado(id=cliente_id)

        assert evento.id == cliente_id
        assert isinstance(evento, Evento)

    def test_deve_criar_evento_cliente_atualizado(self):
        """Deve criar evento ClienteAtualizado."""
        cliente_id = uuid4()
        evento = ClienteAtualizado(id=cliente_id)

        assert evento.id == cliente_id
        assert isinstance(evento, Evento)

    def test_deve_criar_evento_cliente_removido(self):
        """Deve criar evento ClienteRemovido."""
        cliente_id = uuid4()
        evento = ClienteRemovido(id=cliente_id)

        assert evento.id == cliente_id
        assert isinstance(evento, Evento)
