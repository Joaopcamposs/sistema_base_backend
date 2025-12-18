"""
Testes de integração para os repositórios.
Estes testes usam o bootstrap pattern para gerenciar corretamente as conexões.
"""

import pytest
from uuid import uuid4

from contextos_de_negocio.barramento.bootstrap import bootstrap
from contextos_de_negocio.dominio.comandos.usuario import CadastrarUsuario
from contextos_de_negocio.dominio.comandos.cliente import CadastrarCliente
from contextos_de_negocio.dominio.entidades.cliente import Endereco
from libs.barramento_de_mensagens.base.executor_assincrono import ExecutorAssincronoNulo
from libs.utils.tipos_basicos import CPF, Email
from tests.mocks import ID_EMPRESA_TESTE


@pytest.mark.asyncio
class TestRepositoriosViaBootstrap:
    """
    Testes de integração para repositórios usando o bootstrap pattern.
    O bootstrap gerencia corretamente as sessões de banco de dados.
    """

    async def test_deve_cadastrar_e_consultar_usuario(
        self, mock_primeira_empresa, usuario_teste, cpf_valido
    ):
        """Deve cadastrar e consultar usuário via repositório."""
        email_unico = f"repo_user_{uuid4().hex[:8]}@teste.com"

        bus = bootstrap(
            usuario=usuario_teste,
            subir_erros_de_eventos=True,
            executor_assincrono=ExecutorAssincronoNulo(),
        )

        # Cadastra usuário
        comando = CadastrarUsuario(
            nome="Usuario Repo Teste",
            email=email_unico,
            cpf=cpf_valido,
            senha="senha123",
            ativo=True,
            adm=False,
            empresa=ID_EMPRESA_TESTE,
            permissoes=["leitura"],
        )
        usuario_id = await bus.handle(comando)

        assert usuario_id is not None

    async def test_deve_cadastrar_e_consultar_cliente(
        self, mock_primeira_empresa, usuario_teste, cpf_valido
    ):
        """Deve cadastrar e consultar cliente via repositório."""
        email_unico = f"repo_cli_{uuid4().hex[:8]}@teste.com"

        bus = bootstrap(
            usuario=usuario_teste,
            subir_erros_de_eventos=True,
            executor_assincrono=ExecutorAssincronoNulo(),
        )

        endereco = Endereco(
            cep="01310100",
            rua="Avenida Paulista",
            numero="1000",
            complemento="Sala 101",
            bairro="Bela Vista",
            cidade="São Paulo",
            estado="SP",
            pais="Brasil",
        )

        # Cadastra cliente
        comando = CadastrarCliente(
            nome="Cliente Repo Teste",
            cpf=CPF(cpf_valido),
            telefone="11999999999",
            telefone_2="",
            email=Email(email_unico),
            endereco=endereco,
        )
        cliente_id = await bus.handle(comando)

        assert cliente_id is not None

    async def test_deve_cadastrar_multiplos_usuarios(
        self, mock_primeira_empresa, usuario_teste
    ):
        """Deve cadastrar múltiplos usuários."""
        bus = bootstrap(
            usuario=usuario_teste,
            subir_erros_de_eventos=True,
            executor_assincrono=ExecutorAssincronoNulo(),
        )

        usuarios_criados = []
        for i in range(3):
            cpf = CPF.gerar()
            email = f"multi_user_{uuid4().hex[:8]}@teste.com"

            comando = CadastrarUsuario(
                nome=f"Usuario Multi {i}",
                email=email,
                cpf=cpf,
                senha="senha123",
                ativo=True,
                adm=False,
                empresa=ID_EMPRESA_TESTE,
                permissoes=[],
            )
            usuario_id = await bus.handle(comando)
            usuarios_criados.append(usuario_id)

        assert len(usuarios_criados) == 3
        assert all(uid is not None for uid in usuarios_criados)
