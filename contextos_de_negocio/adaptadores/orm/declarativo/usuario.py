from __future__ import annotations

from uuid import uuid4

from sqlalchemy import UUID, String, Boolean, ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from libs.ddd.adaptadores.orm.declarativo import Base, CamposBaseDB


class UsuarioDB(Base, CamposBaseDB):
    __tablename__ = "usuario"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, unique=True, default=uuid4)
    empresa: Mapped[UUID] = mapped_column(UUID, nullable=False)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, index=True
    )
    cpf: Mapped[str] = mapped_column(String(11), nullable=False, unique=True, index=True)
    senha: Mapped[str] = mapped_column(String(255), nullable=False)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    adm: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    permissoes: Mapped[list[str]] = mapped_column(
        ARRAY(String), nullable=False, default=[]
    )

    def __repr__(self):
        return f"Usuario(email={self.email}, id={self.id})"

    def __hash__(self):
        return hash(self.id)
