from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from contextos_de_negocio.dominio.agregados.registro_de_servico import RegistroDeServico
from contextos_de_negocio.dominio.entidades.usuario import UsuarioEntidade
from contextos_de_negocio.dominio.eventos.sessao_de_servicos import (
    SessaoDeServicosAtualizado,
    SessaoDeServicosRemovido,
    SessaoDeServicosCriado,
)
from libs.ddd.dominio.agregado import Agregado
from libs.utils.tipos_basicos import TipoDeOperacao


@dataclass
class SessaoDeServicos(Agregado):
    id: UUID
    id_cliente: UUID
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
    registros: list[RegistroDeServico] = field(default_factory=list)

    def __post_init__(self) -> None:
        self._usa_soft_delete = True

    def __hash__(self) -> int:
        return hash(self.id)

    @classmethod
    def retornar_agregado_para_cadastro(
        cls,
        id_cliente: UUID,
        cpf_do_cliente: str,
        nome_do_cliente: str,
        data_inicio_da_realizacao: datetime,
        data_final_da_realizacao: datetime,
        valor_total: Decimal,
        valor_desconto: Decimal,
        valor_pago: Decimal,
        valor_restante: Decimal,
        forma_de_pagamento: str,
        observacoes: str,
        registros: list[RegistroDeServico],
    ) -> "SessaoDeServicos":
        return SessaoDeServicos(
            id=uuid4(),
            id_cliente=id_cliente,
            cpf_do_cliente=cpf_do_cliente,
            nome_do_cliente=nome_do_cliente,
            data_inicio_da_realizacao=data_inicio_da_realizacao,
            data_final_da_realizacao=data_final_da_realizacao,
            valor_total=valor_total,
            valor_desconto=valor_desconto,
            valor_pago=valor_pago,
            valor_restante=valor_restante,
            forma_de_pagamento=forma_de_pagamento,
            observacoes=observacoes,
            registros=registros,
        )

    def cadastrar(self, usuario: UsuarioEntidade) -> None:
        self._tipo_de_operacao = TipoDeOperacao.INSERCAO

        self.criado_por = usuario.id
        self.criado_em = datetime.now()

        self.add_event(SessaoDeServicosCriado(id=self.id))

    def atualizar(
        self,
        nome_do_cliente: str,
        data_inicio_da_realizacao: datetime,
        data_final_da_realizacao: datetime,
        valor_total: Decimal,
        valor_desconto: Decimal,
        valor_pago: Decimal,
        valor_restante: Decimal,
        forma_de_pagamento: str,
        observacoes: str,
        registros: list[RegistroDeServico],
        usuario: UsuarioEntidade,
    ) -> None:
        self._tipo_de_operacao = TipoDeOperacao.ATUALIZACAO

        self.nome_do_cliente = nome_do_cliente
        self.data_inicio_da_realizacao = data_inicio_da_realizacao
        self.data_final_da_realizacao = data_final_da_realizacao
        self.valor_total = valor_total
        self.valor_desconto = valor_desconto
        self.valor_pago = valor_pago
        self.valor_restante = valor_restante
        self.forma_de_pagamento = forma_de_pagamento
        self.observacoes = observacoes
        self.registros = registros

        self.modificado_por = usuario.id
        self.ultima_modificacao_em = datetime.now()

        self.add_event(SessaoDeServicosAtualizado(id=self.id))

    def remover(self, usuario: UsuarioEntidade) -> None:
        self._tipo_de_operacao = TipoDeOperacao.REMOCAO

        self.modificado_por = usuario.id
        self.ultima_modificacao_em = datetime.now()

        self.deletado_por = usuario.id
        self.deletado_em = datetime.now()

        self.add_event(SessaoDeServicosRemovido(id=self.id))
