from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
from contextos_de_negocio.dominio.entidades.usuario import UsuarioEntidade
from contextos_de_negocio.dominio.eventos.usuario import (
    UsuarioCriado,
    UsuarioAtualizado,
    UsuarioRemovido,
)
from libs.utils.tipos_basicos import Email, TipoDeOperacao
from libs.ddd.dominio.agregado import Agregado, SegurancaDoUsuario


@dataclass
class Usuario(Agregado, SegurancaDoUsuario):
    id: UUID
    empresa: UUID
    nome: str
    email: str
    cpf: str
    senha_hash: str
    ativo: bool
    adm: bool
    permissoes: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self._usa_soft_delete = True

    def __hash__(self) -> int:
        return hash(self.id)

    @classmethod
    def retornar_agregado_para_cadastro(
        cls,
        empresa: UUID,
        nome: str,
        email: str,
        cpf: str,
        senha: str,
        ativo: bool,
        adm: bool,
        permissoes: list[str],
    ) -> "Usuario":
        senha = cls.criptografar_senha(senha)
        email = Email(email)
        return Usuario(
            empresa=empresa,
            nome=nome,
            email=email,
            cpf=cpf,
            senha_hash=senha,
            adm=adm,
            ativo=ativo,
            permissoes=permissoes,
            id=uuid4(),
            _tipo_de_operacao=TipoDeOperacao.INSERCAO,
        )

    def cadastrar(self, usuario: UsuarioEntidade) -> None:
        self.criado_por = None  # nao registraremos o usuario que criou
        self.criado_em = datetime.now()

        self.add_event(UsuarioCriado(id=self.id))

    def atualizar(
        self,
        nome: str,
        email: str,
        cpf: str,
        senha: str,
        adm: bool,
        ativo: bool,
        permissoes: list[str],
        usuario: UsuarioEntidade,
    ) -> None:
        self._tipo_de_operacao = TipoDeOperacao.ATUALIZACAO

        self.nome = nome
        self.email = Email(email)
        self.cpf = cpf  # todo desativado temporariamente
        self.senha_hash = self.criptografar_senha(senha)
        self.ativo = ativo
        self.adm = adm
        self.permissoes = permissoes

        self.modificado_por = usuario.id
        self.ultima_modificacao_em = datetime.now()

        self.add_event(UsuarioAtualizado(id=self.id))

    def remover(self, usuario: UsuarioEntidade) -> None:
        self._tipo_de_operacao = TipoDeOperacao.REMOCAO

        self.modificado_por = usuario.id
        self.ultima_modificacao_em = datetime.now()

        self.deletado_por = usuario.id
        self.deletado_em = datetime.now()

        self.add_event(UsuarioRemovido(id=self.id))


@dataclass
class UsuarioPublico(Agregado, SegurancaDoUsuario):
    id: UUID
    empresa: UUID
    email_criptografado: bytes
    email_hash: str
    senha_hash: str
    ativo: bool

    def __post_init__(self) -> None:
        self._usa_soft_delete = True

    def __hash__(self) -> int:
        return hash(self.id)

    @classmethod
    def retornar_agregado_para_cadastro(
        cls,
        usuario: Usuario,
    ) -> "UsuarioPublico":
        email_criptografado = cls.criptografar_email(usuario.email)
        email_hash = cls.hash_email(usuario.email)

        return UsuarioPublico(
            id=usuario.id,
            empresa=usuario.empresa,
            email_criptografado=email_criptografado,
            email_hash=email_hash,
            senha_hash=usuario.senha_hash,
            ativo=usuario.ativo,
            criado_em=usuario.criado_em,
            criado_por=usuario.criado_por,
            _tipo_de_operacao=TipoDeOperacao.INSERCAO,
        )
