from datetime import datetime
from sqlalchemy import UUID, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

Base = declarative_base()


class CamposBaseDB:
    criado_por: Mapped[UUID] = mapped_column(UUID, nullable=True)
    criado_em: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    ultima_modificacao_em: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    modificado_por: Mapped[UUID] = mapped_column(UUID, nullable=True)
    deletado_em: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=False)
    deletado_por: Mapped[UUID] = mapped_column(UUID, nullable=True)
