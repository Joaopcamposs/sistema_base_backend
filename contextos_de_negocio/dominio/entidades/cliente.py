from dataclasses import dataclass
from uuid import UUID

from libs.ddd.dominio.agregado import CamposBase
from libs.utils.tipos_basicos import CPF, Email


@dataclass(kw_only=True)
class Endereco:
    cep: str
    rua: str
    numero: str
    complemento: str
    bairro: str
    cidade: str
    estado: str
    pais: str

    def __repr__(self) -> str:
        return f"{self.rua}, {self.numero} - {self.bairro}, {self.cidade}/{self.estado}"


@dataclass(kw_only=True)
class ClienteEntidade(CamposBase):
    id: UUID
    nome: str
    cpf: CPF
    telefone: str
    telefone_2: str
    email: Email
    endereco: Endereco
