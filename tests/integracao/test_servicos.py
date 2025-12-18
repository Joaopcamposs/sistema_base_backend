"""
Testes de integração para os serviços (executores).
"""

import pytest
from uuid import uuid4

from contextos_de_negocio.barramento.bootstrap import bootstrap
from contextos_de_negocio.dominio.comandos.usuario import (
    CadastrarUsuario,
    AtualizarUsuario,
    RemoverUsuario,
)
from contextos_de_negocio.dominio.comandos.cliente import (
    CadastrarCliente,
    AtualizarCliente,
    RemoverCliente,
)
from contextos_de_negocio.dominio.entidades.cliente import Endereco
from contextos_de_negocio.dominio.excecoes import (
    UsuarioNaoEncontrado,
    ClienteNaoEncontrado,
)
from libs.barramento_de_mensagens.base.executor_assincrono import ExecutorAssincronoNulo
from libs.utils.tipos_basicos import CPF, Email
from tests.mocks import ID_EMPRESA_TESTE


@pytest.mark.asyncio
class TestServicoUsuarioIntegracao:
    """Testes de integração para o serviço de usuário."""

    async def test_deve_cadastrar_usuario_via_comando(self, usuario_teste, cpf_valido):
        """Deve cadastrar usuário através do comando."""
        email_unico = f"cmd_cad_{uuid4().hex[:8]}@teste.com"

        bus = bootstrap(
            usuario=usuario_teste,
            subir_erros_de_eventos=True,
            executor_assincrono=ExecutorAssincronoNulo(),
        )

        comando = CadastrarUsuario(
            nome="Usuario Via Comando",
            email=email_unico,
            cpf=cpf_valido,
            senha="senha123",
            ativo=True,
            adm=False,
            empresa=ID_EMPRESA_TESTE,
            permissoes=["leitura"],
        )

        resultado = await bus.handle(comando)

        assert resultado is not None
        # resultado deve ser o UUID do usuário criado

    async def test_deve_atualizar_usuario_via_comando(self, usuario_teste, cpf_valido):
        """Deve atualizar usuário através do comando."""
        email_original = f"cmd_upd_{uuid4().hex[:8]}@teste.com"
        email_novo = f"cmd_upd_novo_{uuid4().hex[:8]}@teste.com"

        bus = bootstrap(
            usuario=usuario_teste,
            subir_erros_de_eventos=True,
            executor_assincrono=ExecutorAssincronoNulo(),
        )

        # Primeiro cadastra
        comando_cadastrar = CadastrarUsuario(
            nome="Usuario Para Atualizar",
            email=email_original,
            cpf=cpf_valido,
            senha="senha123",
            ativo=True,
            adm=False,
            empresa=ID_EMPRESA_TESTE,
            permissoes=[],
        )
        usuario_id = await bus.handle(comando_cadastrar)

        # Depois atualiza
        comando_atualizar = AtualizarUsuario(
            nome="Usuario Atualizado Via Comando",
            email=email_novo,
            cpf=cpf_valido,
            senha="nova_senha",
            ativo=True,
            adm=True,
            permissoes=["admin"],
            id=usuario_id,
            email_antigo=email_original,
        )

        resultado = await bus.handle(comando_atualizar)

        assert resultado == usuario_id

    async def test_deve_remover_usuario_via_comando(self, usuario_teste, cpf_valido):
        """Deve remover usuário através do comando."""
        email_unico = f"cmd_rem_{uuid4().hex[:8]}@teste.com"

        bus = bootstrap(
            usuario=usuario_teste,
            subir_erros_de_eventos=True,
            executor_assincrono=ExecutorAssincronoNulo(),
        )

        # Primeiro cadastra
        comando_cadastrar = CadastrarUsuario(
            nome="Usuario Para Remover",
            email=email_unico,
            cpf=cpf_valido,
            senha="senha123",
            ativo=True,
            adm=False,
            empresa=ID_EMPRESA_TESTE,
            permissoes=[],
        )
        usuario_id = await bus.handle(comando_cadastrar)

        # Depois remove
        comando_remover = RemoverUsuario(
            id=usuario_id,
            email=email_unico,
        )

        resultado = await bus.handle(comando_remover)

        assert resultado == usuario_id

    async def test_deve_falhar_ao_remover_usuario_inexistente(self, usuario_teste):
        """Deve falhar ao tentar remover usuário inexistente."""
        bus = bootstrap(
            usuario=usuario_teste,
            subir_erros_de_eventos=True,
            executor_assincrono=ExecutorAssincronoNulo(),
        )

        comando = RemoverUsuario(
            id=uuid4(),
            email="nao_existe@teste.com",
        )

        with pytest.raises(UsuarioNaoEncontrado):
            await bus.handle(comando)


@pytest.mark.asyncio
class TestServicoClienteIntegracao:
    """Testes de integração para o serviço de cliente."""

    @pytest.fixture
    def endereco_teste(self):
        """Fixture para criar endereço de teste."""
        return Endereco(
            cep="01310100",
            rua="Avenida Paulista",
            numero="1000",
            complemento="Sala 101",
            bairro="Bela Vista",
            cidade="São Paulo",
            estado="SP",
            pais="Brasil",
        )

    async def test_deve_cadastrar_cliente_via_comando(
        self, usuario_teste, cpf_valido, endereco_teste
    ):
        """Deve cadastrar cliente através do comando."""
        email_unico = f"cli_cmd_{uuid4().hex[:8]}@teste.com"

        bus = bootstrap(
            usuario=usuario_teste,
            subir_erros_de_eventos=True,
            executor_assincrono=ExecutorAssincronoNulo(),
        )

        comando = CadastrarCliente(
            nome="Cliente Via Comando",
            cpf=CPF(cpf_valido),
            telefone="11999999999",
            telefone_2="",
            email=Email(email_unico),
            endereco=endereco_teste,
        )

        resultado = await bus.handle(comando)

        assert resultado is not None

    async def test_deve_atualizar_cliente_via_comando(
        self, usuario_teste, cpf_valido, endereco_teste
    ):
        """Deve atualizar cliente através do comando."""
        email_original = f"cli_upd_{uuid4().hex[:8]}@teste.com"
        email_novo = f"cli_upd_novo_{uuid4().hex[:8]}@teste.com"

        bus = bootstrap(
            usuario=usuario_teste,
            subir_erros_de_eventos=True,
            executor_assincrono=ExecutorAssincronoNulo(),
        )

        # Primeiro cadastra
        comando_cadastrar = CadastrarCliente(
            nome="Cliente Para Atualizar",
            cpf=CPF(cpf_valido),
            telefone="11999999999",
            telefone_2="",
            email=Email(email_original),
            endereco=endereco_teste,
        )
        cliente_id = await bus.handle(comando_cadastrar)

        # Depois atualiza
        novo_endereco = Endereco(
            cep="04538133",
            rua="Rua Nova",
            numero="200",
            complemento="Apt 10",
            bairro="Itaim",
            cidade="São Paulo",
            estado="SP",
            pais="Brasil",
        )

        comando_atualizar = AtualizarCliente(
            nome="Cliente Atualizado Via Comando",
            cpf=CPF(cpf_valido),
            telefone="11888888888",
            telefone_2="1133333333",
            email=Email(email_novo),
            endereco=novo_endereco,
            id=cliente_id,
            cpf_busca=cpf_valido,
        )

        resultado = await bus.handle(comando_atualizar)

        assert resultado == cliente_id

    async def test_deve_remover_cliente_via_comando(
        self, usuario_teste, cpf_valido, endereco_teste
    ):
        """Deve remover cliente através do comando."""
        email_unico = f"cli_rem_{uuid4().hex[:8]}@teste.com"

        bus = bootstrap(
            usuario=usuario_teste,
            subir_erros_de_eventos=True,
            executor_assincrono=ExecutorAssincronoNulo(),
        )

        # Primeiro cadastra
        comando_cadastrar = CadastrarCliente(
            nome="Cliente Para Remover",
            cpf=CPF(cpf_valido),
            telefone="11999999999",
            telefone_2="",
            email=Email(email_unico),
            endereco=endereco_teste,
        )
        cliente_id = await bus.handle(comando_cadastrar)

        # Depois remove
        comando_remover = RemoverCliente(
            id=cliente_id,
            cpf=cpf_valido,
        )

        resultado = await bus.handle(comando_remover)

        assert resultado == cliente_id

    async def test_deve_falhar_ao_remover_cliente_inexistente(self, usuario_teste):
        """Deve falhar ao tentar remover cliente inexistente."""
        bus = bootstrap(
            usuario=usuario_teste,
            subir_erros_de_eventos=True,
            executor_assincrono=ExecutorAssincronoNulo(),
        )

        comando = RemoverCliente(
            id=uuid4(),
            cpf="52998224725",
        )

        with pytest.raises(ClienteNaoEncontrado):
            await bus.handle(comando)


@pytest.mark.asyncio
class TestFluxoCompletoIntegracao:
    """Testes de fluxo completo de integração."""

    async def test_fluxo_completo_usuario(self, usuario_teste):
        """Testa fluxo completo: cadastrar, consultar, atualizar, remover usuário."""
        cpf = CPF.gerar()
        email_original = f"fluxo_{uuid4().hex[:8]}@teste.com"
        email_atualizado = f"fluxo_upd_{uuid4().hex[:8]}@teste.com"

        bus = bootstrap(
            usuario=usuario_teste,
            subir_erros_de_eventos=True,
            executor_assincrono=ExecutorAssincronoNulo(),
        )

        # 1. Cadastrar
        comando_cadastrar = CadastrarUsuario(
            nome="Usuario Fluxo Completo",
            email=email_original,
            cpf=cpf,
            senha="senha123",
            ativo=True,
            adm=False,
            empresa=ID_EMPRESA_TESTE,
            permissoes=["leitura"],
        )
        usuario_id = await bus.handle(comando_cadastrar)
        assert usuario_id is not None

        # 2. Atualizar
        comando_atualizar = AtualizarUsuario(
            nome="Usuario Fluxo Atualizado",
            email=email_atualizado,
            cpf=cpf,
            senha="nova_senha",
            ativo=True,
            adm=True,
            permissoes=["admin", "leitura"],
            id=usuario_id,
            email_antigo=email_original,
        )
        resultado_atualizacao = await bus.handle(comando_atualizar)
        assert resultado_atualizacao == usuario_id

        # 3. Remover
        comando_remover = RemoverUsuario(
            id=usuario_id,
            email=email_atualizado,
        )
        resultado_remocao = await bus.handle(comando_remover)
        assert resultado_remocao == usuario_id

        # 4. Verificar que não encontra mais
        with pytest.raises(UsuarioNaoEncontrado):
            await bus.handle(RemoverUsuario(id=usuario_id, email=email_atualizado))
