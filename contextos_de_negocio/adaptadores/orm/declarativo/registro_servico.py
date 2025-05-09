from decimal import Decimal
from datetime import datetime
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import ForeignKey, DateTime, Numeric, String, UUID, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column

from libs.ddd.adaptadores.orm.declarativo import Base, CamposBaseDB

if TYPE_CHECKING:
    from contextos_de_negocio.adaptadores.orm.declarativo import (
        ServicoDB,
        HistoricoServicosDB,
    )


class RegistroServicoDB(Base, CamposBaseDB):
    """
    Classe que representa um registro de procedimento realizado em uma ficha clínica.
    Ela guarda os dados do registro na época em que o procedimento foi realizado.
    """

    __tablename__ = "registro_servico"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, unique=True, default=uuid4)

    # ligação à ficha clínica
    historico_servico_id: Mapped[UUID] = mapped_column(
        ForeignKey("historico_servicos.id"), nullable=False
    )
    # referência ao modelo, para auditoria, mas NÃO usamos seus dados dinâmicos
    servico_id: Mapped[UUID] = mapped_column(ForeignKey("servico.id"), nullable=False)

    # snapshot dos campos do modelo no momento da realização
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    valor: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    descricao: Mapped[str] = mapped_column(Text, nullable=False)
    data_realizacao: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), default=datetime.now, nullable=False
    )

    # relacoes
    historico: Mapped["HistoricoServicosDB"] = relationship(
        "HistoricoServicosDB", back_populates="registros"
    )
    servico: Mapped["ServicoDB"] = relationship("ServicoDB", back_populates="registros")
