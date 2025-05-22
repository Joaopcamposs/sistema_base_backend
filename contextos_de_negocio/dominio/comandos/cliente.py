from dataclasses import dataclass
from uuid import UUID

from barramento_de_mensagens.base.barramento import Comando

from contextos_de_negocio.dominio.entidades.cliente import Endereco
from libs.utils.tipos_basicos import Email, CPF


@dataclass
class CadastrarCliente(Comando):
    nome: str
    cpf: CPF
    telefone: str
    telefone_2: str
    email: Email
    endereco: Endereco


@dataclass
class AtualizarCliente(Comando):
    nome: str
    cpf: CPF
    telefone: str
    telefone_2: str
    email: Email
    endereco: Endereco
    # campos de busca
    id: UUID | None = None
    cpf_busca: str | None = None


@dataclass
class RemoverCliente(Comando):
    id: UUID | None = None
    cpf: str | None = None
