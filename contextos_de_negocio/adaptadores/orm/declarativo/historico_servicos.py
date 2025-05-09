from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import ForeignKey, UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

from libs.ddd.adaptadores.orm.declarativo import CamposBaseDB, Base

if TYPE_CHECKING:
    from contextos_de_negocio.adaptadores.orm.declarativo import (
        ClienteDB,
        RegistroServicoDB,
    )


class HistoricoServicosDB(Base, CamposBaseDB):
    __tablename__ = "historico_servicos"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, unique=True, default=uuid4)
    cliente_id: Mapped[UUID] = mapped_column(
        ForeignKey("cliente.id"), nullable=False, unique=True
    )

    # relacoes
    cliente: Mapped["ClienteDB"] = relationship("ClienteDB", back_populates="historico")
    registros: Mapped[list["RegistroServicoDB"]] = relationship(
        "RegistroServicoDB", back_populates="historico"
    )
