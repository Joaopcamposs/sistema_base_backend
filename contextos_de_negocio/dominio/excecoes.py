from dataclasses import dataclass

from libs.utils.excecoes import FeedbackUsuario
from fastapi import status


@dataclass
class UsuarioNaoEncontrado(FeedbackUsuario):
    detail: str = "Usuario não encontrado"
    status_code: int = status.HTTP_404_NOT_FOUND


@dataclass
class UsuarioJaCadastrado(FeedbackUsuario):
    detail: str = "Email de Usuario já existente"
    status_code: int = status.HTTP_409_CONFLICT


@dataclass
class EmpresaNaoEncontrada(FeedbackUsuario):
    detail: str = "Empresa não encontrada"
    status_code: int = status.HTTP_404_NOT_FOUND


@dataclass
class EmpresaJaCadastrada(FeedbackUsuario):
    detail: str = "Email de Empresa já existente"
    status_code: int = status.HTTP_409_CONFLICT


@dataclass
class ClienteNaoEncontrado(FeedbackUsuario):
    detail: str = "Cliente não encontrado"
    status_code: int = status.HTTP_404_NOT_FOUND


@dataclass
class ClienteJaCadastrado(FeedbackUsuario):
    detail: str = "{tipo_de_campo} de Cliente já existente"
    status_code: int = status.HTTP_409_CONFLICT

    def __init__(self, tipo_de_campo: str):
        # cpf ou email
        self.detail = self.detail.format(tipo_de_campo=tipo_de_campo)


@dataclass
class ServicoNaoEncontrado(FeedbackUsuario):
    detail: str = "Servico não encontrado"
    status_code: int = status.HTTP_404_NOT_FOUND


@dataclass
class ServicoJaCadastrado(FeedbackUsuario):
    detail: str = "Codigo de Servico já existente"
    status_code: int = status.HTTP_409_CONFLICT


@dataclass
class RegistroDeServicoNaoEncontrado(FeedbackUsuario):
    detail: str = "RegistroDeServico não encontrado"
    status_code: int = status.HTTP_404_NOT_FOUND


@dataclass
class RegistroDeServicoJaCadastrado(FeedbackUsuario):
    detail: str = "id de RegistroDeServico já existente"
    status_code: int = status.HTTP_409_CONFLICT


@dataclass
class SessaoDeServicosNaoEncontrado(FeedbackUsuario):
    detail: str = "SessaoDeServicos não encontrado"
    status_code: int = status.HTTP_404_NOT_FOUND


@dataclass
class SessaoDeServicosJaCadastrado(FeedbackUsuario):
    detail: str = "id de SessaoDeServicos já existente"
    status_code: int = status.HTTP_409_CONFLICT
