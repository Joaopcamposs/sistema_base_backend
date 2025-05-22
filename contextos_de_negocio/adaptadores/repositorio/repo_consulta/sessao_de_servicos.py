from sqlalchemy import select
from uuid import UUID

from sqlalchemy.orm import selectinload

from contextos_de_negocio.adaptadores.orm.declarativo.sessao_de_servicos import (
    SessaoDeServicosDB,
)
from contextos_de_negocio.dominio.entidades.sessao_de_servicos import (
    SessaoDeServicosEntidade,
)
from contextos_de_negocio.dominio.entidades.registro_de_servico import (
    RegistroDeServicoEntidade,
)
from libs.ddd.adaptadores.repositorio.repositorio import RepositorioConsulta
from libs.ddd.adaptadores.visualizadores.visualizadores import Filtros
from libs.utils.constantes import NAO_DELETADO


class SessaoDeServicosRepoConsulta(RepositorioConsulta):
    async def consultar_um_por_id(self, id: UUID) -> SessaoDeServicosEntidade | None:
        async with self.session as session:
            sessao = (
                await session.execute(
                    select(SessaoDeServicosDB)
                    .where(
                        SessaoDeServicosDB.id == id,
                        SessaoDeServicosDB.deletado_em.is_(None),
                    )
                    .options(select(SessaoDeServicosDB.registros))
                )
            ).scalar_one_or_none()
            if not sessao:
                return None

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
                for registro in sessao.registros
            ]

            sessao_entidade = SessaoDeServicosEntidade(
                id=sessao.id,
                codigo=sessao.codigo,
                cpf_do_cliente=sessao.cpf_do_cliente,
                nome_do_cliente=sessao.nome_do_cliente,
                data_inicio_da_realizacao=sessao.data_inicio_da_realizacao,
                data_final_da_realizacao=sessao.data_final_da_realizacao,
                valor_total=sessao.valor_total,
                valor_desconto=sessao.valor_desconto,
                valor_pago=sessao.valor_pago,
                valor_restante=sessao.valor_restante,
                forma_de_pagamento=sessao.forma_de_pagamento,
                observacoes=sessao.observacoes,
                registros=registros_entidade,
            )

        return sessao_entidade

    async def consultar_por_filtros(
        self, filtros: Filtros
    ) -> list[SessaoDeServicosEntidade]:
        async with self.session as session:
            sessoes = (
                (
                    await session.execute(
                        select(SessaoDeServicosDB)
                        .filter_by(**filtros, **NAO_DELETADO)
                        .options(selectinload(SessaoDeServicosDB.registros))
                    )
                )
                .scalars()
                .all()
            )

            sessoes_entidade = []
            for sessao in sessoes:
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
                    for registro in sessao.registros
                ]

                sessoes_entidade.append(
                    SessaoDeServicosEntidade(
                        id=sessao.id,
                        codigo=sessao.codigo,
                        cpf_do_cliente=sessao.cpf_do_cliente,
                        nome_do_cliente=sessao.nome_do_cliente,
                        data_inicio_da_realizacao=sessao.data_inicio_da_realizacao,
                        data_final_da_realizacao=sessao.data_final_da_realizacao,
                        valor_total=sessao.valor_total,
                        valor_desconto=sessao.valor_desconto,
                        valor_pago=sessao.valor_pago,
                        valor_restante=sessao.valor_restante,
                        forma_de_pagamento=sessao.forma_de_pagamento,
                        observacoes=sessao.observacoes,
                        registros=registros_entidade,
                    )
                )

        return sessoes_entidade
