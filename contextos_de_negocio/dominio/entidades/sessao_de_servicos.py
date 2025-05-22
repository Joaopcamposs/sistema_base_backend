from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from decimal import Decimal

from contextos_de_negocio.dominio.entidades.registro_de_servico import (
    RegistroDeServicoEntidade,
)


@dataclass(kw_only=True)
class SessaoDeServicosEntidade:
    id: UUID
    codigo: int
    cpf_do_cliente: str
    nome_do_cliente: str
    data_inicio_da_realizacao: datetime
    data_final_da_realizacao: datetime
    valor_total: Decimal
    valor_desconto: Decimal
    valor_pago: Decimal
    valor_restante: Decimal
    forma_de_pagamento: str
    observacoes: str
    registros: list[RegistroDeServicoEntidade]
