from sqlalchemy import select

from contextos_de_negocio.adaptadores.orm.declarativo.usuario import (
    UsuarioDB,
    UsuarioPublicoDB,
)
from contextos_de_negocio.dominio.entidades.usuario import (
    UsuarioEntidade,
    UsuarioPublicoEntidade,
)
from libs.ddd.adaptadores.repositorio.repositorio import RepositorioConsulta
from libs.ddd.adaptadores.visualizadores.visualizadores import Filtros
from libs.utils.constantes import NAO_DELETADO


class UsuarioRepoConsulta(RepositorioConsulta):
    async def consultar_usuario_publico_por_email(
        self, email: str
    ) -> UsuarioPublicoEntidade | None:
        email_hash = UsuarioPublicoEntidade.hash_email(email)
        async with self.session as session:
            usuario = (
                await session.execute(
                    select(UsuarioPublicoDB).where(
                        UsuarioPublicoDB.email_hash == email_hash,
                        UsuarioPublicoDB.deletado_em.is_(None),
                    )
                )
            ).scalar_one_or_none()
            if not usuario:
                return None

            usuario_entidade = UsuarioPublicoEntidade(
                id=usuario.id,
                empresa=usuario.empresa_id,
                ativo=usuario.ativo,
                email_criptografado=usuario.email_criptografado,
                email_hash=usuario.email_hash,
                _senha_hash=usuario.senha_hash,
            )

        if (
            UsuarioPublicoEntidade.descriptografar_email(
                usuario_entidade.email_criptografado
            )
            == email
        ):
            return usuario_entidade
        return None

    async def consultar_um_por_email(self, email: str) -> UsuarioEntidade | None:
        async with self.session as session:
            usuario = (
                await session.execute(
                    select(UsuarioDB).where(
                        UsuarioDB.email == email, UsuarioDB.deletado_em.is_(None)
                    )
                )
            ).scalar_one_or_none()
            if not usuario:
                return None

            usuario_entidade = UsuarioEntidade(
                id=usuario.id,
                empresa=usuario.empresa_id,
                nome=usuario.nome,
                email=usuario.email,
                cpf=usuario.cpf,
                adm=usuario.adm,
                ativo=usuario.ativo,
                _senha_hash=usuario.senha,
            )

        return usuario_entidade

    async def consultar_um_por_filtros(self, filtros: Filtros) -> UsuarioEntidade | None:
        async with self.session as session:
            usuario = (
                await session.execute(
                    select(UsuarioDB).filter_by(**filtros, **NAO_DELETADO)
                )
            ).scalar_one_or_none()
            if not usuario:
                return None

            usuario_entidade = UsuarioEntidade(
                id=usuario.id,
                empresa=usuario.empresa_id,
                nome=usuario.nome,
                email=usuario.email,
                cpf=usuario.cpf,
                adm=usuario.adm,
                ativo=usuario.ativo,
                _senha_hash=usuario.senha,
            )

        return usuario_entidade

    async def consultar_por_filtros(self, filtros: Filtros) -> list[UsuarioEntidade]:
        async with self.session as session:
            usuarios = (
                (
                    await session.execute(
                        select(UsuarioDB).filter_by(**filtros, **NAO_DELETADO)
                    )
                )
                .scalars()
                .all()
            )

            usuarios_entidade = [
                UsuarioEntidade(
                    id=usuario.id,
                    empresa=usuario.empresa_id,
                    nome=usuario.nome,
                    email=usuario.email,
                    cpf=usuario.cpf,
                    adm=usuario.adm,
                    ativo=usuario.ativo,
                    _senha_hash=usuario.senha,
                )
                for usuario in usuarios
            ]

        return usuarios_entidade
