from sqlalchemy import select

from contextos_de_negocio.adaptadores.orm.declarativo.usuario import UsuarioDB
from contextos_de_negocio.dominio.entidades.usuario import UsuarioEntidade
from libs.ddd.adaptadores.repositorio.repositorio import RepositorioConsulta
from libs.ddd.adaptadores.visualizadores.visualizadores import Filtros
from libs.utils.constantes import NAO_DELETADO


class UsuarioRepoConsulta(RepositorioConsulta):
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
                empresa=usuario.empresa,
                nome=usuario.nome,
                email=usuario.email,
                cpf=usuario.cpf,
                adm=usuario.adm,
                ativo=usuario.ativo,
                _senha=usuario.senha,
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
                empresa=usuario.empresa,
                nome=usuario.nome,
                email=usuario.email,
                cpf=usuario.cpf,
                adm=usuario.adm,
                ativo=usuario.ativo,
                _senha=usuario.senha,
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
                    empresa=usuario.empresa,
                    nome=usuario.nome,
                    email=usuario.email,
                    cpf=usuario.cpf,
                    adm=usuario.adm,
                    ativo=usuario.ativo,
                    _senha=usuario.senha,
                )
                for usuario in usuarios
            ]

        return usuarios_entidade
