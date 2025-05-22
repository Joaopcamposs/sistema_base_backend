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
        SessaoDeServicosDB,
    )


class RegistroDeServicoDB(Base, CamposBaseDB):
    __tablename__ = "registro_de_servico"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, unique=True, default=uuid4)

    # Ligação à sessão de serviços
    id_sessao_de_servicos: Mapped[UUID] = mapped_column(
        ForeignKey("sessao_de_servicos.id"), nullable=False
    )
    codigo_sessao_de_servicos: Mapped[int] = mapped_column(
        ForeignKey("sessao_de_servicos.codigo"), nullable=False
    )
    id_servico: Mapped[UUID] = mapped_column(ForeignKey("servico.id"), nullable=False)
    codigo_servico: Mapped[str] = mapped_column(
        ForeignKey("servico.codigo"), nullable=False
    )

    # Snapshot dos campos do modelo no momento da realização
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    valor: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    descricao: Mapped[str] = mapped_column(Text, nullable=False)
    data_realizacao: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now, nullable=False
    )

    # Relacionamentos
    sessao: Mapped["SessaoDeServicosDB"] = relationship(
        "SessaoDeServicosDB",
        back_populates="registros",
        foreign_keys="[RegistroDeServicoDB.id_sessao_de_servicos]",  # Especifica a FK correta
    )
    servico: Mapped["ServicoDB"] = relationship(
        "ServicoDB",
        back_populates="registros",
        foreign_keys="[RegistroDeServicoDB.id_servico]",  # Especifica a FK correta
    )
