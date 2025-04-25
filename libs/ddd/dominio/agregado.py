import hashlib
import os
from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from libs.utils.constantes import pwd_context, AES_KEY
from libs.utils.tipos_basicos import TipoDeOperacao


@dataclass(kw_only=True)
class CamposBase(ABC):
    criado_por: UUID | None = None
    criado_em: datetime | None = None
    modificado_por: UUID | None = None
    ultima_modificacao_em: datetime | None = None
    deletado_por: UUID | None = None
    deletado_em: datetime | None = None


@dataclass(kw_only=True)
class Agregado(CamposBase):
    eventos: list["Evento"] = field(default_factory=list)  # noqa: F821
    _tipo_de_operacao: TipoDeOperacao | None = None
    _usa_soft_delete: bool = True

    def to_dict(self) -> dict:
        dados = {
            key: value for key, value in self.__dict__.items() if not key.startswith("_")
        }
        tipo_para_nao_converter = (str, int, float, bool, dict, list, tuple)

        def _converter_elemento(elemento):
            if hasattr(elemento, "to_dict"):
                return elemento.to_dict()
            elif isinstance(elemento, list):
                return [_converter_elemento(sub_elemento) for sub_elemento in elemento]
            else:
                return (
                    str(elemento)
                    if type(elemento) not in tipo_para_nao_converter
                    else elemento
                )

        dados_convertidos = {
            key: _converter_elemento(value) for key, value in dados.items()
        }

        return dados_convertidos

    def add_event(self, event: "Evento"):  # noqa: F821
        from libs.ddd.barramento import Evento

        assert issubclass(type(event), Evento)
        self.eventos = getattr(self, "eventos", [])
        self.eventos.append(event)


@dataclass
class SegurancaDoUsuario:
    def verificar_senha(self, senha: str) -> bool:
        if getattr(self, "senha_hash", None):
            senha_hash = self.senha_hash  # noqa: F821
        else:
            senha_hash = self._senha_hash  # noqa: F821

        senhas_conferem = pwd_context.verify(secret=senha, hash=senha_hash)
        return senhas_conferem

    @staticmethod
    def criptografar_senha(senha: str) -> str:
        senha_criptografada = pwd_context.hash(secret=senha)
        return senha_criptografada

    @staticmethod
    def hash_email(email: str) -> str:
        return hashlib.sha256(email.strip().lower().encode()).hexdigest()

    @staticmethod
    def criptografar_email(email: str) -> bytes:
        aesgcm = AESGCM(AES_KEY)
        nonce = os.urandom(12)
        ct = aesgcm.encrypt(nonce, email.encode(), None)
        return nonce + ct

    @staticmethod
    def descriptografar_email(email: bytes) -> str:
        aesgcm = AESGCM(AES_KEY)
        nonce, ct = email[:12], email[12:]
        return aesgcm.decrypt(nonce, ct, None).decode()
