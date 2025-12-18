"""
Mocks e fixtures para testes.
"""

import pytest
from uuid import UUID

from libs.barramento_de_mensagens.base.executor_assincrono import (
    ExecutorAssincronoNulo,
)
from contextos_de_negocio.dominio.entidades.usuario import UsuarioEntidade
from libs.utils.tipos_basicos import CPF, Email


# IDs fixos para testes
ID_EMPRESA_TESTE = UUID("7529b0ae-81ad-488b-b4ed-ecc094ca5084")
ID_USUARIO_TESTE = UUID("11111111-1111-1111-1111-111111111111")


@pytest.fixture
def executor_assincrono_nulo() -> ExecutorAssincronoNulo:
    """Executor assíncrono nulo para testes."""
    return ExecutorAssincronoNulo()


@pytest.fixture
def usuario_teste() -> UsuarioEntidade:
    """Usuário de teste padrão."""
    return UsuarioEntidade(
        id=ID_USUARIO_TESTE,
        empresa=ID_EMPRESA_TESTE,
        nome="Usuario Teste",
        email=Email("teste@teste.com"),
        cpf=CPF("52998224725"),
        _senha_hash="$2b$12$hash_teste",
        ativo=True,
        adm=True,
        permissoes=[],
    )


@pytest.fixture
def id_empresa_teste() -> UUID:
    """ID da empresa de teste."""
    return ID_EMPRESA_TESTE


@pytest.fixture
def id_usuario_teste() -> UUID:
    """ID do usuário de teste."""
    return ID_USUARIO_TESTE


@pytest.fixture
def cpf_valido() -> str:
    """CPF válido para testes."""
    return CPF.gerar()


@pytest.fixture
def email_teste() -> str:
    """Email de teste."""
    return "teste@teste.com"


@pytest.fixture
def senha_teste() -> str:
    """Senha de teste."""
    return "senha_segura_123"
