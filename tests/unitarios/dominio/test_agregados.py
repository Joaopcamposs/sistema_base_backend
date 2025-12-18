"""
Testes unitários para os agregados do domínio.
"""

from uuid import uuid4

from contextos_de_negocio.dominio.agregados.usuario import Usuario, UsuarioPublico
from contextos_de_negocio.dominio.agregados.empresa import Empresa
from contextos_de_negocio.dominio.agregados.cliente import Cliente
from contextos_de_negocio.dominio.entidades.cliente import Endereco
from contextos_de_negocio.dominio.eventos.usuario import (
    UsuarioCriado,
    UsuarioAtualizado,
    UsuarioRemovido,
)
from contextos_de_negocio.dominio.eventos.empresa import EmpresaCriada
from contextos_de_negocio.dominio.eventos.cliente import (
    ClienteCriado,
    ClienteAtualizado,
    ClienteRemovido,
)
from libs.utils.tipos_basicos import CPF, Email, TipoDeOperacao


class TestUsuarioAgregado:
    """Testes para o agregado Usuario."""

    def test_deve_criar_usuario_para_cadastro(self):
        """Deve criar um usuário válido para cadastro."""
        empresa_id = uuid4()

        usuario = Usuario.retornar_agregado_para_cadastro(
            empresa=empresa_id,
            nome="João da Silva",
            email=Email("joao@teste.com"),
            cpf=CPF("52998224725"),
            senha="senha123",
            ativo=True,
            adm=False,
            permissoes=["leitura"],
        )

        assert usuario.empresa == empresa_id
        assert usuario.nome == "João da Silva"
        assert str(usuario.email) == "joao@teste.com"
        assert usuario.ativo is True
        assert usuario.adm is False
        assert usuario.permissoes == ["leitura"]
        assert usuario.senha_hash != "senha123"  # senha deve estar criptografada
        assert usuario.id is not None

    def test_deve_cadastrar_usuario_e_gerar_evento(self, usuario_teste):
        """Deve cadastrar usuário e gerar evento UsuarioCriado."""
        empresa_id = uuid4()

        usuario = Usuario.retornar_agregado_para_cadastro(
            empresa=empresa_id,
            nome="Maria Santos",
            email=Email("maria@teste.com"),
            cpf=CPF("52998224725"),
            senha="senha123",
            ativo=True,
            adm=True,
            permissoes=[],
        )

        usuario.cadastrar(usuario=usuario_teste)

        assert usuario._tipo_de_operacao == TipoDeOperacao.INSERCAO
        assert usuario.criado_por == usuario_teste.id
        assert usuario.criado_em is not None
        assert len(usuario.eventos) == 1
        assert isinstance(usuario.eventos[0], UsuarioCriado)
        assert usuario.eventos[0].id == usuario.id

    def test_deve_atualizar_usuario_e_gerar_evento(self, usuario_teste):
        """Deve atualizar usuário e gerar evento UsuarioAtualizado."""
        empresa_id = uuid4()

        usuario = Usuario.retornar_agregado_para_cadastro(
            empresa=empresa_id,
            nome="Carlos Teste",
            email=Email("carlos@teste.com"),
            cpf=CPF("52998224725"),
            senha="senha123",
            ativo=True,
            adm=False,
            permissoes=[],
        )
        usuario.cadastrar(usuario=usuario_teste)
        usuario.eventos.clear()  # limpa eventos anteriores

        usuario.atualizar(
            nome="Carlos Atualizado",
            email=Email("carlos.novo@teste.com"),
            cpf=CPF("52998224725"),
            senha="nova_senha",
            adm=True,
            ativo=True,
            permissoes=["admin"],
            usuario=usuario_teste,
        )

        assert usuario._tipo_de_operacao == TipoDeOperacao.ATUALIZACAO
        assert usuario.nome == "Carlos Atualizado"
        assert str(usuario.email) == "carlos.novo@teste.com"
        assert usuario.adm is True
        assert usuario.permissoes == ["admin"]
        assert usuario.modificado_por == usuario_teste.id
        assert usuario.ultima_modificacao_em is not None
        assert len(usuario.eventos) == 1
        assert isinstance(usuario.eventos[0], UsuarioAtualizado)

    def test_deve_remover_usuario_e_gerar_evento(self, usuario_teste):
        """Deve remover usuário (soft delete) e gerar evento UsuarioRemovido."""
        empresa_id = uuid4()

        usuario = Usuario.retornar_agregado_para_cadastro(
            empresa=empresa_id,
            nome="Usuario Para Remover",
            email=Email("remover@teste.com"),
            cpf=CPF("52998224725"),
            senha="senha123",
            ativo=True,
            adm=False,
            permissoes=[],
        )
        usuario.cadastrar(usuario=usuario_teste)
        usuario.eventos.clear()

        usuario.remover(usuario=usuario_teste)

        assert usuario._tipo_de_operacao == TipoDeOperacao.REMOCAO
        assert usuario.deletado_por == usuario_teste.id
        assert usuario.deletado_em is not None
        assert len(usuario.eventos) == 1
        assert isinstance(usuario.eventos[0], UsuarioRemovido)

    def test_deve_verificar_senha_correta(self):
        """Deve verificar senha correta do usuário."""
        usuario = Usuario.retornar_agregado_para_cadastro(
            empresa=uuid4(),
            nome="Teste Senha",
            email=Email("senha@teste.com"),
            cpf=CPF("52998224725"),
            senha="minha_senha_secreta",
            ativo=True,
            adm=False,
            permissoes=[],
        )

        assert usuario.verificar_senha("minha_senha_secreta") is True
        assert usuario.verificar_senha("senha_errada") is False

    def test_deve_converter_usuario_para_dict(self):
        """Deve converter usuário para dicionário."""
        empresa_id = uuid4()

        usuario = Usuario.retornar_agregado_para_cadastro(
            empresa=empresa_id,
            nome="Teste Dict",
            email=Email("dict@teste.com"),
            cpf=CPF("52998224725"),
            senha="senha123",
            ativo=True,
            adm=False,
            permissoes=["leitura"],
        )

        usuario_dict = usuario.to_dict()

        assert usuario_dict["nome"] == "Teste Dict"
        assert usuario_dict["email"] == "dict@teste.com"
        assert usuario_dict["ativo"] is True
        # eventos é um campo público (não começa com _), então aparece no dict
        assert "eventos" in usuario_dict


class TestEmpresaAgregado:
    """Testes para o agregado Empresa."""

    def test_deve_criar_empresa_para_cadastro(self):
        """Deve criar uma empresa válida para cadastro."""
        empresa = Empresa.retornar_agregado_para_cadastro(
            razao_social="Empresa Teste LTDA",
            nome_fantasia="Empresa Teste",
            nome_responsavel="João Responsável",
            email=Email("empresa@teste.com"),
            cpf=CPF("52998224725"),
            cnpj=None,
            ativo=True,
        )

        assert empresa.razao_social == "Empresa Teste LTDA"
        assert empresa.nome_fantasia == "Empresa Teste"
        assert empresa.nome_responsavel == "João Responsável"
        assert str(empresa.email) == "empresa@teste.com"
        assert empresa.ativo is True
        assert empresa.id is not None

    def test_deve_cadastrar_empresa_e_gerar_eventos(self, usuario_teste):
        """Deve cadastrar empresa e gerar eventos."""
        empresa = Empresa.retornar_agregado_para_cadastro(
            razao_social="Nova Empresa LTDA",
            nome_fantasia="Nova Empresa",
            nome_responsavel="Maria Responsável",
            email=Email("nova@empresa.com"),
            cpf=CPF("52998224725"),
            cnpj=None,
            ativo=True,
            _eh_primeira_empresa=True,
        )

        empresa.cadastrar(usuario=usuario_teste, senha="senha_empresa")

        assert empresa._tipo_de_operacao == TipoDeOperacao.INSERCAO
        assert empresa.criado_por == usuario_teste.id
        assert empresa.criado_em is not None
        # Deve ter evento EmpresaCriada e ChegouAHoraDeCriarUsuarioInicialDaEmpresa
        assert len(empresa.eventos) >= 2
        assert isinstance(empresa.eventos[0], EmpresaCriada)

    def test_deve_remover_empresa_e_gerar_evento(self, usuario_teste):
        """Deve remover empresa e gerar evento."""
        empresa = Empresa.retornar_agregado_para_cadastro(
            razao_social="Empresa Para Remover",
            nome_fantasia=None,
            nome_responsavel="Responsável",
            email=Email("remover@empresa.com"),
            cpf=CPF("52998224725"),
            cnpj=None,
            ativo=True,
        )
        empresa.cadastrar(usuario=usuario_teste, senha="senha")
        empresa.eventos.clear()

        empresa.remover(usuario=usuario_teste)

        assert empresa._tipo_de_operacao == TipoDeOperacao.REMOCAO
        assert empresa.deletado_por == usuario_teste.id
        assert empresa.deletado_em is not None


class TestClienteAgregado:
    """Testes para o agregado Cliente."""

    def test_deve_criar_cliente_para_cadastro(self):
        """Deve criar um cliente válido para cadastro."""
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

        cliente = Cliente.retornar_agregado_para_cadastro(
            nome="Cliente Teste",
            cpf=CPF("52998224725"),
            telefone="11999999999",
            telefone_2="1133333333",
            email=Email("cliente@teste.com"),
            endereco=endereco,
        )

        assert cliente.nome == "Cliente Teste"
        assert str(cliente.email) == "cliente@teste.com"
        assert cliente.telefone == "11999999999"
        assert cliente.endereco.cidade == "São Paulo"
        assert cliente.id is not None

    def test_deve_cadastrar_cliente_e_gerar_evento(self, usuario_teste):
        """Deve cadastrar cliente e gerar evento ClienteCriado."""
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

        cliente = Cliente.retornar_agregado_para_cadastro(
            nome="Novo Cliente",
            cpf=CPF("52998224725"),
            telefone="11888888888",
            telefone_2="",
            email=Email("novo.cliente@teste.com"),
            endereco=endereco,
        )

        cliente.cadastrar(usuario=usuario_teste)

        assert cliente._tipo_de_operacao == TipoDeOperacao.INSERCAO
        assert cliente.criado_por == usuario_teste.id
        assert cliente.criado_em is not None
        assert len(cliente.eventos) == 1
        assert isinstance(cliente.eventos[0], ClienteCriado)

    def test_deve_atualizar_cliente_e_gerar_evento(self, usuario_teste):
        """Deve atualizar cliente e gerar evento ClienteAtualizado."""
        endereco = Endereco(
            cep="01310100",
            rua="Rua Original",
            numero="50",
            complemento=None,
            bairro="Centro",
            cidade="São Paulo",
            estado="SP",
            pais="Brasil",
        )

        cliente = Cliente.retornar_agregado_para_cadastro(
            nome="Cliente Original",
            cpf=CPF("52998224725"),
            telefone="11777777777",
            telefone_2="",
            email=Email("original@teste.com"),
            endereco=endereco,
        )
        cliente.cadastrar(usuario=usuario_teste)
        cliente.eventos.clear()

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

        cliente.atualizar(
            nome="Cliente Atualizado",
            cpf=CPF("52998224725"),
            telefone="11666666666",
            telefone_2="1122222222",
            email=Email("atualizado@teste.com"),
            endereco=novo_endereco,
            usuario=usuario_teste,
        )

        assert cliente._tipo_de_operacao == TipoDeOperacao.ATUALIZACAO
        assert cliente.nome == "Cliente Atualizado"
        assert cliente.endereco.rua == "Rua Nova"
        assert cliente.modificado_por == usuario_teste.id
        assert len(cliente.eventos) == 1
        assert isinstance(cliente.eventos[0], ClienteAtualizado)

    def test_deve_remover_cliente_e_gerar_evento(self, usuario_teste):
        """Deve remover cliente e gerar evento ClienteRemovido."""
        endereco = Endereco(
            cep="01310100",
            rua="Rua Teste",
            numero="1",
            complemento=None,
            bairro="Centro",
            cidade="São Paulo",
            estado="SP",
            pais="Brasil",
        )

        cliente = Cliente.retornar_agregado_para_cadastro(
            nome="Cliente Para Remover",
            cpf=CPF("52998224725"),
            telefone="11555555555",
            telefone_2="",
            email=Email("remover@teste.com"),
            endereco=endereco,
        )
        cliente.cadastrar(usuario=usuario_teste)
        cliente.eventos.clear()

        cliente.remover(usuario=usuario_teste)

        assert cliente._tipo_de_operacao == TipoDeOperacao.REMOCAO
        assert cliente.deletado_por == usuario_teste.id
        assert cliente.deletado_em is not None
        assert len(cliente.eventos) == 1
        assert isinstance(cliente.eventos[0], ClienteRemovido)


class TestUsuarioPublicoAgregado:
    """Testes para o agregado UsuarioPublico."""

    def test_deve_criar_usuario_publico_a_partir_de_usuario(self, usuario_teste):
        """Deve criar um UsuarioPublico a partir de um Usuario."""
        usuario = Usuario.retornar_agregado_para_cadastro(
            empresa=uuid4(),
            nome="Usuario Para Publico",
            email=Email("publico@teste.com"),
            cpf=CPF("52998224725"),
            senha="senha123",
            ativo=True,
            adm=False,
            permissoes=[],
        )
        usuario.cadastrar(usuario=usuario_teste)

        usuario_publico = UsuarioPublico.retornar_agregado_para_cadastro(usuario=usuario)

        assert usuario_publico.id == usuario.id
        assert usuario_publico.empresa == usuario.empresa
        assert usuario_publico.email_hash is not None
        assert usuario_publico.email_criptografado is not None
        assert usuario_publico.senha_hash == usuario.senha_hash
        assert usuario_publico.ativo == usuario.ativo

    def test_deve_descriptografar_email(self, usuario_teste):
        """Deve descriptografar email do UsuarioPublico."""
        email_original = "teste_cripto@teste.com"

        usuario = Usuario.retornar_agregado_para_cadastro(
            empresa=uuid4(),
            nome="Usuario Cripto",
            email=Email(email_original),
            cpf=CPF("52998224725"),
            senha="senha123",
            ativo=True,
            adm=False,
            permissoes=[],
        )
        usuario.cadastrar(usuario=usuario_teste)

        usuario_publico = UsuarioPublico.retornar_agregado_para_cadastro(usuario=usuario)
        email_descriptografado = usuario_publico.descriptografar_email(
            usuario_publico.email_criptografado
        )

        assert email_descriptografado == email_original
