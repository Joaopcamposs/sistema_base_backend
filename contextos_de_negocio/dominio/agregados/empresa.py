from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from contextos_de_negocio.dominio.eventos.empresa import (
    EmpresaCriada,
    EmpresaAtualizada,
    EmpresaRemovida,
)

from contextos_de_negocio.dominio.entidades.usuario import UsuarioEntidade
from contextos_de_negocio.dominio.eventos.usuario import (
    ChegouAHoraDeCriarUsuarioInicialDaEmpresa,
    ChegouAHoraDeCriarUsuarioADMDaEmpresa,
)
from libs.utils.constantes import PREFIXO_USUARIO_ADM
from libs.utils.tipos_basicos import Email, TipoDeOperacao
from libs.ddd.dominio.agregado import Agregado


@dataclass(kw_only=True)
class Empresa(Agregado):
    id: UUID
    razao_social: str
    nome_responsavel: str
    email: str
    ativo: bool
    cpf: str
    nome_fantasia: str | None = None
    cnpj: str | None = None

    _eh_primeira_empresa: bool = False

    def __post_init__(self) -> None:
        self._usa_soft_delete = True

    def __hash__(self) -> int:
        return hash(self.id)

    @classmethod
    def retornar_agregado_para_cadastro(
        cls,
        razao_social: str,
        nome_fantasia: str | None,
        nome_responsavel: str,
        email: str,
        cpf: str,
        cnpj: str | None,
        ativo: bool,
        id: UUID | None = None,
        _eh_primeira_empresa: bool = False,
    ) -> "Empresa":
        email = Email(email)
        return Empresa(
            razao_social=razao_social,
            nome_fantasia=nome_fantasia,
            nome_responsavel=nome_responsavel,
            email=email,
            cpf=cpf,
            cnpj=cnpj,
            ativo=ativo,
            id=id or uuid4(),
            _tipo_de_operacao=TipoDeOperacao.INSERCAO,
            _eh_primeira_empresa=_eh_primeira_empresa,
        )

    def cadastrar(self, usuario: UsuarioEntidade, senha: str) -> None:
        self.criado_por = None  # nao registraremos o usuario que criou
        self.criado_em = datetime.now()

        self.add_event(EmpresaCriada(id=self.id))
        self.add_event(
            ChegouAHoraDeCriarUsuarioInicialDaEmpresa(
                nome=self.nome_responsavel,
                email=self.email,
                cpf=self.cpf,
                senha=senha,
                ativo=True,
                adm=True,
                empresa=self.id,
            )
        )
        if not self._eh_primeira_empresa:
            self.add_event(
                ChegouAHoraDeCriarUsuarioADMDaEmpresa(
                    empresa=self.id, email=f"{PREFIXO_USUARIO_ADM}@{str(self.id)}.com"
                )
            )

    def atualizar(
        self,
        razao_social: str,
        nome_fantasia: str | None,
        nome_responsavel: str,
        email: str,
        cpf: str,
        cnpj: str | None,
        ativo: bool,
        usuario: UsuarioEntidade,
    ) -> None:
        self._tipo_de_operacao = TipoDeOperacao.ATUALIZACAO

        self.razao_social = razao_social
        self.nome_fantasia = nome_fantasia
        self.nome_responsavel = nome_responsavel
        self.email = Email(email)
        self.cpf = cpf  # todo desativado temporariamente
        self.cnpj = cnpj
        self.ativo = ativo

        self.modificado_por = None  # nao registraremos o usuario que modificou
        self.ultima_modificacao_em = datetime.now()

        self.add_event(EmpresaAtualizada(id=self.id))

    def remover(self, usuario: UsuarioEntidade) -> None:
        self._tipo_de_operacao = TipoDeOperacao.REMOCAO

        self.modificado_por = usuario.id
        self.ultima_modificacao_em = datetime.now()

        self.deletado_por = usuario.id
        self.deletado_em = datetime.now()

        self.add_event(EmpresaRemovida(id=self.id))
