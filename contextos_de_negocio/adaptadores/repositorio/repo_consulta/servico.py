from sqlalchemy import select

from contextos_de_negocio.adaptadores.orm.declarativo.servico import ServicoDB
from contextos_de_negocio.dominio.entidades.servico import ServicoEntidade
from libs.ddd.adaptadores.repositorio.repositorio import RepositorioConsulta
from libs.ddd.adaptadores.visualizadores.visualizadores import Filtros
from libs.utils.constantes import NAO_DELETADO


class ServicoRepoConsulta(RepositorioConsulta):
    async def consultar_um_por_codigo(self, codigo: str) -> ServicoEntidade | None:
        async with self.session as session:
            servico = (
                await session.execute(
                    select(ServicoDB).where(
                        ServicoDB.codigo == codigo, ServicoDB.deletado_em.is_(None)
                    )
                )
            ).scalar_one_or_none()
            if not servico:
                return None

            servico_entidade = ServicoEntidade(
                id=servico.id,
                codigo=servico.codigo,
                nome=servico.nome,
                descricao=servico.descricao,
                valor=servico.valor,
            )

        return servico_entidade

    async def consultar_um_por_filtros(self, filtros: Filtros) -> ServicoEntidade | None:
        async with self.session as session:
            servico = (
                await session.execute(
                    select(ServicoDB).filter_by(**filtros, **NAO_DELETADO)
                )
            ).scalar_one_or_none()
            if not servico:
                return None

            servico_entidade = ServicoEntidade(
                id=servico.id,
                codigo=servico.codigo,
                nome=servico.nome,
                descricao=servico.descricao,
                valor=servico.valor,
            )

        return servico_entidade

    async def consultar_por_filtros(self, filtros: Filtros) -> list[ServicoEntidade]:
        async with self.session as session:
            servicos = (
                (
                    await session.execute(
                        select(ServicoDB).filter_by(**filtros, **NAO_DELETADO)
                    )
                )
                .scalars()
                .all()
            )

            servicos_entidade = [
                ServicoEntidade(
                    id=servico.id,
                    codigo=servico.codigo,
                    nome=servico.nome,
                    descricao=servico.descricao,
                    valor=servico.valor,
                )
                for servico in servicos
            ]

        return servicos_entidade
