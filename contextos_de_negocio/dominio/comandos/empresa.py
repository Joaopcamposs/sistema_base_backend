from dataclasses import dataclass
from uuid import UUID

from barramento_de_mensagens.base.barramento import Comando


@dataclass
class CadastrarEmpresa(Comando):
    """
    Para cadastrar uma nova empresa, deve ser gerado um id, passar esse id para o schema no bootstrap
    e informar o mesmo ID aqui no comando.
    """

    razao_social: str
    nome_responsavel: str
    ativo: bool
    cpf: str
    email: str
    senha: str
    id: UUID
    cnpj: str | None = None
    nome_fantasia: str | None = None
    deve_criar_usuario: bool = True
    _eh_primeira_empresa: bool = False


@dataclass
class AtualizarEmpresa(Comando):
    nome_responsavel: str
    email: str
    ativo: bool
    razao_social: str
    cpf: str
    nome_fantasia: str | None = None
    cnpj: str | None = None
    # campos de busca
    id: UUID | None = None
    email_antigo: str | None = None


@dataclass
class RemoverEmpresa(Comando):
    id: UUID | None = None
    email: str | None = None
