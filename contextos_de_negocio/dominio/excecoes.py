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
    detail: str = "CPF de Cliente já existente"
    status_code: int = status.HTTP_409_CONFLICT


@dataclass
class ServicoNaoEncontrado(FeedbackUsuario):
    detail: str = "Servico não encontrado"
    status_code: int = status.HTTP_404_NOT_FOUND


@dataclass
class ServicoJaCadastrado(FeedbackUsuario):
    detail: str = "Codigo de Servico já existente"
    status_code: int = status.HTTP_409_CONFLICT
