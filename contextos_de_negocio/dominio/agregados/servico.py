from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from contextos_de_negocio.dominio.entidades.usuario import UsuarioEntidade
from contextos_de_negocio.dominio.eventos.servico import (
    ServicoCriado,
    ServicoAtualizado,
    ServicoRemovido,
)
from libs.ddd.dominio.agregado import Agregado
from libs.utils.tipos_basicos import TipoDeOperacao


@dataclass
class Servico(Agregado):
    id: UUID
    codigo: str
    nome: str
    descricao: str
    valor: Decimal

    def __post_init__(self) -> None:
        self._usa_soft_delete = True

    def __hash__(self) -> int:
        return hash(self.id)

    @classmethod
    def retornar_agregado_para_cadastro(
        cls,
        codigo: str,
        nome: str,
        descricao: str,
        valor: Decimal,
    ) -> "Servico":
        return Servico(
            codigo=codigo,
            nome=nome,
            descricao=descricao,
            valor=valor,
            id=uuid4(),
        )

    def cadastrar(self, usuario: UsuarioEntidade) -> None:
        self._tipo_de_operacao = TipoDeOperacao.INSERCAO

        self.criado_por = usuario.id
        self.criado_em = datetime.now()

        self.add_event(ServicoCriado(id=self.id))

    def atualizar(
        self,
        codigo: str,
        nome: str,
        descricao: str,
        valor: Decimal,
        usuario: UsuarioEntidade,
    ) -> None:
        self._tipo_de_operacao = TipoDeOperacao.ATUALIZACAO

        self.codigo = codigo
        self.nome = nome
        self.descricao = descricao
        self.valor = valor

        self.modificado_por = usuario.id
        self.ultima_modificacao_em = datetime.now()

        self.add_event(ServicoAtualizado(id=self.id))

    def remover(self, usuario: UsuarioEntidade) -> None:
        self._tipo_de_operacao = TipoDeOperacao.REMOCAO

        self.modificado_por = usuario.id
        self.ultima_modificacao_em = datetime.now()

        self.deletado_por = usuario.id
        self.deletado_em = datetime.now()

        self.add_event(ServicoRemovido(id=self.id))
