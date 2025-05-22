from pydantic import UUID4

from contextos_de_negocio.dominio.entidades.sessao_de_servicos import (
    SessaoDeServicosEntidade,
)
from contextos_de_negocio.barramento.unidade_de_trabalho import UnidadeDeTrabalho
from libs.ddd.adaptadores.visualizadores.visualizadores import Filtros


async def listar_sessoes_por_id_e_cliente(
    unidade_de_trabalho: UnidadeDeTrabalho,
    id: UUID4 | None = None,
    cpf_cliente: str | None = None,
) -> list[SessaoDeServicosEntidade]:
    from contextos_de_negocio import Dominio, SessaoDeServicosRepoConsulta

    filtros = Filtros(
        {
            "id": id,
            "cpf_cliente": cpf_cliente,
        }
    )

    async with unidade_de_trabalho(Dominio.sessao_de_servicos) as uow:
        repo_consulta: SessaoDeServicosRepoConsulta = uow.view_repo

        sessoes = await repo_consulta.consultar_por_filtros(filtros=filtros)

    return sessoes
