from pydantic import UUID4

from contextos_de_negocio.dominio.entidades.servico import ServicoEntidade
from contextos_de_negocio.barramento.unidade_de_trabalho import UnidadeDeTrabalho
from libs.ddd.adaptadores.visualizadores.visualizadores import Filtros


async def listar_servicos_por_id_e_codigo(
    unidade_de_trabalho: UnidadeDeTrabalho,
    id: UUID4 | None = None,
    codigo: str | None = None,
) -> list[ServicoEntidade]:
    from contextos_de_negocio import Dominio, ServicoRepoConsulta

    filtros = Filtros(
        {
            "id": id,
            "codigo": codigo,
        }
    )

    async with unidade_de_trabalho(Dominio.servico) as uow:
        repo_consulta: ServicoRepoConsulta = uow.view_repo

        servicos = await repo_consulta.consultar_por_filtros(filtros=filtros)

    return servicos
