from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from decimal import Decimal

from libs.barramento_de_mensagens.base.barramento import Comando

from contextos_de_negocio.dominio.entidades.registro_de_servico import (
    RegistroDeServicoEntidade,
)


@dataclass
class CadastrarSessaoDeServicos(Comando):
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


@dataclass
class AtualizarSessaoDeServicos(Comando):
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
    # campos de busca
    id: UUID | None = None


@dataclass
class RemoverSessaoDeServicos(Comando):
    id: UUID | None = None
