from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from contextos_de_negocio.dominio.entidades.cliente import Endereco
from contextos_de_negocio.dominio.entidades.usuario import UsuarioEntidade
from contextos_de_negocio.dominio.eventos.cliente import (
    ClienteCriado,
    ClienteAtualizado,
    ClienteRemovido,
)
from libs.ddd.dominio.agregado import Agregado
from libs.utils.tipos_basicos import CPF, Email, TipoDeOperacao


@dataclass
class Cliente(Agregado):
    id: UUID
    nome: str
    cpf: CPF
    telefone: str
    telefone_2: str
    email: Email
    endereco: Endereco

    def __post_init__(self) -> None:
        self._usa_soft_delete = True

    def __hash__(self) -> int:
        return hash(self.id)

    @classmethod
    def retornar_agregado_para_cadastro(
        cls,
        nome: str,
        cpf: CPF,
        telefone: str,
        telefone_2: str,
        email: Email,
        endereco: Endereco,
    ) -> "Cliente":
        email = Email(email)
        cpf = CPF(cpf)
        return Cliente(
            nome=nome,
            cpf=cpf,
            telefone=telefone,
            telefone_2=telefone_2,
            email=email,
            endereco=endereco,
            id=uuid4(),
        )

    def cadastrar(self, usuario: UsuarioEntidade) -> None:
        self._tipo_de_operacao = TipoDeOperacao.INSERCAO

        self.criado_por = usuario.id
        self.criado_em = datetime.now()

        self.add_event(ClienteCriado(id=self.id))

    def atualizar(
        self,
        nome: str,
        cpf: CPF,
        telefone: str,
        telefone_2: str,
        email: Email,
        endereco: Endereco,
        usuario: UsuarioEntidade,
    ) -> None:
        self._tipo_de_operacao = TipoDeOperacao.ATUALIZACAO

        self.nome = nome
        self.cpf = CPF(cpf)
        self.telefone = telefone
        self.telefone_2 = telefone_2
        self.email = Email(email)
        self.endereco = endereco

        self.modificado_por = usuario.id
        self.ultima_modificacao_em = datetime.now()

        self.add_event(ClienteAtualizado(id=self.id))

    def remover(self, usuario: UsuarioEntidade) -> None:
        self._tipo_de_operacao = TipoDeOperacao.REMOCAO

        self.modificado_por = usuario.id
        self.ultima_modificacao_em = datetime.now()

        self.deletado_por = usuario.id
        self.deletado_em = datetime.now()

        self.add_event(ClienteRemovido(id=self.id))
