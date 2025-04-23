from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from contextos_de_negocio.dominio.entidades.usuario import UsuarioEntidade
from contextos_de_negocio.dominio.eventos.usuario import (
    UsuarioCriado,
    UsuarioAtualizado,
    UsuarioRemovido,
)
from libs.utils.constantes import pwd_context
from libs.utils.tipos_basicos import Email, TipoDeOperacao, CPF
from libs.ddd.dominio.agregado import Agregado


@dataclass
class Usuario(Agregado):
    id: UUID
    empresa: UUID
    nome: str
    email: str
    cpf: str
    senha: str
    ativo: bool
    adm: bool
    permissoes: list[str] = field(default_factory=list)

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
            senha=senha,
            adm=adm,
            ativo=ativo,
            permissoes=permissoes,
            id=uuid4(),
            _tipo_de_operacao=TipoDeOperacao.INSERCAO,
        )

    def cadastrar(self, usuario: UsuarioEntidade) -> None:
        self.criado_por = usuario.id
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
        self.cpf = CPF(cpf)
        self.senha = senha
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

    def verificar_senha(self, senha: str) -> bool:
        senhas_conferem = pwd_context.verify(secret=senha, hash=self.senha)
        return senhas_conferem

    @staticmethod
    def criptografar_senha(senha: str) -> str:
        senha_criptografada = pwd_context.hash(secret=senha)
        return senha_criptografada
