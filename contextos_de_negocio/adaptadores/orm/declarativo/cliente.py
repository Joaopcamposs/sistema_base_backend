from uuid import uuid4

from sqlalchemy import String, UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

from libs.ddd.adaptadores.orm.declarativo import CamposBaseDB, Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from contextos_de_negocio.adaptadores.orm.declarativo import HistoricoServicosDB


class ClienteDB(Base, CamposBaseDB):
    __tablename__ = "cliente"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, unique=True, default=uuid4)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    cpf: Mapped[str] = mapped_column(String(11), nullable=False, unique=True, index=True)
    telefone: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    telefone_2: Mapped[str] = mapped_column(String(255), nullable=True, default=None)
    email: Mapped[str] = mapped_column(String(255), nullable=True, default=None)

    # Campos de endereço
    cep: Mapped[str] = mapped_column(String(255), nullable=True, default=None)
    rua: Mapped[str] = mapped_column(String(255), nullable=False)
    numero: Mapped[str] = mapped_column(String(255), nullable=False)
    complemento: Mapped[str] = mapped_column(String(255), nullable=True, default=None)
    bairro: Mapped[str] = mapped_column(String(255), nullable=False)
    cidade: Mapped[str] = mapped_column(String(255), nullable=False)
    estado: Mapped[str] = mapped_column(String(255), nullable=False)
    pais: Mapped[str] = mapped_column(String(255), nullable=False)

    # cada cliente tem UMA ficha clínica
    historico: Mapped["HistoricoServicosDB"] = relationship(
        "HistoricoServicosDB", back_populates="cliente", uselist=False
    )
