from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import uuid4
from sqlalchemy import ForeignKey, DateTime, String, UUID, Numeric, Sequence
from sqlalchemy.orm import Mapped, mapped_column, relationship
from libs.ddd.adaptadores.orm.declarativo import Base, CamposBaseDB


if TYPE_CHECKING:
    from contextos_de_negocio.adaptadores.orm.declarativo import (
        ClienteDB,
        RegistroDeServicoDB,
    )


class SessaoDeServicosDB(Base, CamposBaseDB):
    __tablename__ = "sessao_de_servicos"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, unique=True, default=uuid4)
    codigo: Mapped[int] = mapped_column(
        Sequence("sessao_de_servicos_codigo_seq"),
        primary_key=True,
        autoincrement=True,
        nullable=False,
        index=True,
        unique=True,
    )
    id_cliente: Mapped[UUID] = mapped_column(ForeignKey("cliente.id"), nullable=False)
    cpf_do_cliente: Mapped[str] = mapped_column(ForeignKey("cliente.cpf"), nullable=False)
    # dados da sessão
    nome_do_cliente: Mapped[str] = mapped_column(String(100), nullable=False)
    data_inicio_da_realizacao: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now, nullable=False
    )
    data_final_da_realizacao: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    valor_total: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    valor_desconto: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    valor_pago: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    valor_restante: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    forma_de_pagamento: Mapped[str] = mapped_column(String(100), nullable=False)
    observacoes: Mapped[str] = mapped_column(String(255), nullable=True)

    # Relacionamentos
    cliente: Mapped["ClienteDB"] = relationship(
        "ClienteDB",
        back_populates="sessoes",
        foreign_keys="[SessaoDeServicosDB.id_cliente]",  # Especifica a FK correta
    )
    registros: Mapped[list["RegistroDeServicoDB"]] = relationship(
        "RegistroDeServicoDB", back_populates="sessao", foreign_keys="[RegistroDeServicoDB.id_sessao_de_servicos]"
    )
