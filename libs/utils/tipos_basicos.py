from enum import Enum
from validate_docbr import CPF as ValidadorDeCPF


class TipoDeOperacao(Enum):
    INSERCAO = "insercao"
    ATUALIZACAO = "atualizacao"
    REMOCAO = "remocao"


class CPF(str):
    def __init__(self, cpf: str = ""):
        self.cpf = self.somente_digitos(cpf)
        self.validar()

    def validar(self) -> None:
        if not ValidadorDeCPF().validate(self.cpf):
            raise ValueError("CPF inválido")

    @staticmethod
    def somente_digitos(cpf: str) -> str:
        return "".join([char for char in cpf if char.isdigit()])

    @staticmethod
    def gerar() -> str:
        cpf_gerado = ValidadorDeCPF().generate()
        return str(cpf_gerado)

    def __str__(self) -> str:
        return self.cpf


class Email(str):
    # apenas para formatar email para lower case com o new
    def __new__(cls, value: str) -> "Email":
        return super().__new__(cls, value.lower())
