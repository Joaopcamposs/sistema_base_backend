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
