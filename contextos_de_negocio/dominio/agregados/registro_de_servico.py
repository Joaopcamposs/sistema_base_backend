from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from contextos_de_negocio.dominio.entidades.usuario import UsuarioEntidade
from contextos_de_negocio.dominio.eventos.registro_de_servico import (
    RegistroDeServicoCriado,
    RegistroDeServicoAtualizado,
    RegistroDeServicoRemovido,
)
from libs.ddd.dominio.agregado import Agregado
from libs.utils.tipos_basicos import TipoDeOperacao


@dataclass
class RegistroDeServico(Agregado):
    id: UUID
    id_sessao_de_servicos: UUID
    codigo_sessao_de_servicos: int
    id_servico: UUID
    codigo_servico: str
    nome: str
    valor: Decimal
    descricao: str
    data_realizacao: datetime

    def __post_init__(self) -> None:
        self._usa_soft_delete = True

    def __hash__(self) -> int:
        return hash(self.id)

    @classmethod
    def retornar_agregado_para_cadastro(
        cls,
        id_sessao_de_servicos: UUID,
        codigo_sessao_de_servicos: int,
        id_servico: UUID,
        codigo_servico: str,
        nome: str,
        valor: Decimal,
        descricao: str,
        data_realizacao: datetime,
    ) -> "RegistroDeServico":
        return RegistroDeServico(
            id=uuid4(),
            id_sessao_de_servicos=id_sessao_de_servicos,
            codigo_sessao_de_servicos=codigo_sessao_de_servicos,
            id_servico=id_servico,
            codigo_servico=codigo_servico,
            nome=nome,
            valor=valor,
            descricao=descricao,
            data_realizacao=data_realizacao,
        )

    def cadastrar(self, usuario: UsuarioEntidade) -> None:
        self._tipo_de_operacao = TipoDeOperacao.INSERCAO

        self.criado_por = usuario.id
        self.criado_em = datetime.now()

        self.add_event(RegistroDeServicoCriado(id=self.id))

    def atualizar(
        self,
        codigo_servico: int,
        nome: str,
        valor: Decimal,
        descricao: str,
        data_realizacao: datetime,
        usuario: UsuarioEntidade,
    ) -> None:
        self._tipo_de_operacao = TipoDeOperacao.ATUALIZACAO

        self.codigo_servico = codigo_servico
        self.nome = nome
        self.valor = valor
        self.descricao = descricao
        self.data_realizacao = data_realizacao

        self.modificado_por = usuario.id
        self.ultima_modificacao_em = datetime.now()

        self.add_event(RegistroDeServicoAtualizado(id=self.id))

    def remover(self, usuario: UsuarioEntidade) -> None:
        self._tipo_de_operacao = TipoDeOperacao.REMOCAO

        self.modificado_por = usuario.id
        self.ultima_modificacao_em = datetime.now()

        self.deletado_por = usuario.id
        self.deletado_em = datetime.now()

        self.add_event(RegistroDeServicoRemovido(id=self.id))
