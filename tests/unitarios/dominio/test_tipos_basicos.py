"""
Testes unitários para os tipos básicos do domínio.
"""

import pytest
from libs.utils.tipos_basicos import CPF, CNPJ, Email, TipoDeOperacao


class TestCPF:
    """Testes para o tipo CPF."""

    def test_deve_criar_cpf_valido(self):
        """Deve criar um CPF válido."""
        cpf = CPF("529.982.247-25")
        assert str(cpf) == "52998224725"

    def test_deve_criar_cpf_valido_somente_digitos(self):
        """Deve criar um CPF válido apenas com dígitos."""
        cpf = CPF("52998224725")
        assert str(cpf) == "52998224725"

    def test_deve_rejeitar_cpf_invalido(self):
        """Deve rejeitar um CPF inválido."""
        with pytest.raises(ValueError, match="CPF inválido"):
            CPF("12345678901")

    def test_deve_rejeitar_cpf_com_digitos_repetidos(self):
        """Deve rejeitar CPF com dígitos repetidos."""
        with pytest.raises(ValueError, match="CPF inválido"):
            CPF("11111111111")

    def test_deve_gerar_cpf_valido(self):
        """Deve gerar um CPF válido aleatório."""
        cpf_gerado = CPF.gerar()
        # Não deve lançar exceção ao criar com o CPF gerado
        cpf = CPF(cpf_gerado)
        assert len(str(cpf)) == 11


class TestCNPJ:
    """Testes para o tipo CNPJ."""

    def test_deve_criar_cnpj_valido(self):
        """Deve criar um CNPJ válido."""
        cnpj = CNPJ("12.345.678/0001-95")
        assert str(cnpj) == "12345678000195"

    def test_deve_retornar_none_para_cnpj_vazio(self):
        """Deve retornar None para CNPJ vazio."""
        cnpj = CNPJ("")
        assert cnpj is None

    def test_deve_retornar_none_para_cnpj_none(self):
        """Deve retornar None para CNPJ None."""
        cnpj = CNPJ(None)
        assert cnpj is None


class TestEmail:
    """Testes para o tipo Email."""

    def test_deve_criar_email_em_lowercase(self):
        """Deve criar email em lowercase."""
        email = Email("TESTE@TESTE.COM")
        assert str(email) == "teste@teste.com"

    def test_deve_criar_email_mixed_case(self):
        """Deve criar email mixed case em lowercase."""
        email = Email("Teste@Teste.Com")
        assert str(email) == "teste@teste.com"

    def test_deve_manter_email_lowercase(self):
        """Deve manter email que já está em lowercase."""
        email = Email("teste@teste.com")
        assert str(email) == "teste@teste.com"


class TestTipoDeOperacao:
    """Testes para o enum TipoDeOperacao."""

    def test_deve_ter_tipo_insercao(self):
        """Deve ter tipo INSERCAO."""
        assert TipoDeOperacao.INSERCAO.value == "insercao"

    def test_deve_ter_tipo_atualizacao(self):
        """Deve ter tipo ATUALIZACAO."""
        assert TipoDeOperacao.ATUALIZACAO.value == "atualizacao"

    def test_deve_ter_tipo_remocao(self):
        """Deve ter tipo REMOCAO."""
        assert TipoDeOperacao.REMOCAO.value == "remocao"
