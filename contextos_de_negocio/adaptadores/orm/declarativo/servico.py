from decimal import Decimal
from uuid import uuid4

from sqlalchemy import String, Numeric, Text, UUID
from sqlalchemy.orm import relationship, mapped_column, Mapped

from libs.ddd.adaptadores.orm.declarativo import Base, CamposBaseDB


class ServicoDB(Base, CamposBaseDB):
    """
    Classe que representa um modelo generico de servico contratado, seja um procedimento,
    caso, consulta ou exame. Deve ser implementada de acordo com o tipo de serviço e sistema.
    """

    __tablename__ = "servico"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, unique=True, default=uuid4)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    descricao: Mapped[str] = mapped_column(Text, nullable=False)
    valor: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    # relacoes
    registros: Mapped[list["RegistroServicoDB"]] = relationship(
        "RegistroServicoDB", back_populates="servico"
    )
