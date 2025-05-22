from sqlalchemy import select
from uuid import UUID

from contextos_de_negocio.adaptadores.orm.declarativo.registro_de_servico import (
    RegistroDeServicoDB,
)
from contextos_de_negocio.dominio.entidades.registro_de_servico import (
    RegistroDeServicoEntidade,
)
from libs.ddd.adaptadores.repositorio.repositorio import RepositorioConsulta
from libs.ddd.adaptadores.visualizadores.visualizadores import Filtros
from libs.utils.constantes import NAO_DELETADO


class RegistroDeServicoRepoConsulta(RepositorioConsulta):
    async def consultar_um_por_id(self, id: UUID) -> RegistroDeServicoEntidade | None:
        async with self.session as session:
            registro = (
                await session.execute(
                    select(RegistroDeServicoDB).where(
                        RegistroDeServicoDB.id == id,
                        RegistroDeServicoDB.deletado_em.is_(None),
                    )
                )
            ).scalar_one_or_none()
            if not registro:
                return None

            registro_entidade = RegistroDeServicoEntidade(
                id=registro.id,
                codigo_sessao_de_servicos=registro.codigo_sessao_de_servicos,
                codigo_servico=registro.codigo_servico,
                nome=registro.nome,
                valor=registro.valor,
                descricao=registro.descricao,
                data_realizacao=registro.data_realizacao,
            )

        return registro_entidade

    async def consultar_um_por_filtros(
        self, filtros: Filtros
    ) -> RegistroDeServicoEntidade | None:
        async with self.session as session:
            registro = (
                await session.execute(
                    select(RegistroDeServicoDB).filter_by(**filtros, **NAO_DELETADO)
                )
            ).scalar_one_or_none()
            if not registro:
                return None

            registro_entidade = RegistroDeServicoEntidade(
                id=registro.id,
                codigo_sessao_de_servicos=registro.codigo_sessao_de_servicos,
                codigo_servico=registro.codigo_servico,
                nome=registro.nome,
                valor=registro.valor,
                descricao=registro.descricao,
                data_realizacao=registro.data_realizacao,
            )

        return registro_entidade

    async def consultar_por_filtros(
        self, filtros: Filtros
    ) -> list[RegistroDeServicoEntidade]:
        async with self.session as session:
            registros = (
                (
                    await session.execute(
                        select(RegistroDeServicoDB).filter_by(**filtros, **NAO_DELETADO)
                    )
                )
                .scalars()
                .all()
            )

            registros_entidade = [
                RegistroDeServicoEntidade(
                    id=registro.id,
                    codigo_sessao_de_servicos=registro.codigo_sessao_de_servicos,
                    codigo_servico=registro.codigo_servico,
                    nome=registro.nome,
                    valor=registro.valor,
                    descricao=registro.descricao,
                    data_realizacao=registro.data_realizacao,
                )
                for registro in registros
            ]

        return registros_entidade
