from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, UUID4

from contextos_de_negocio.pontos_de_entrada.schemas.registro_de_servico import (
    CadastrarRegistroDeServicoSchema,
    LerRegistroDeServicoSchema,
    AtualizarRegistroDeServicoSchema,
)


class CadastrarSessaoDeServicosSchema(BaseModel):
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
    registros: list[CadastrarRegistroDeServicoSchema] | None = None


class AtualizarSessaoDeServicosSchema(BaseModel):
    nome_do_cliente: str
    data_inicio_da_realizacao: datetime
    data_final_da_realizacao: datetime
    valor_total: Decimal
    valor_desconto: Decimal
    valor_pago: Decimal
    valor_restante: Decimal
    forma_de_pagamento: str
    observacoes: str
    registros: list[AtualizarRegistroDeServicoSchema] | None = None


class LerSessaoDeServicosSchema(BaseModel):
    id: UUID4
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
    registros: list[LerRegistroDeServicoSchema]
