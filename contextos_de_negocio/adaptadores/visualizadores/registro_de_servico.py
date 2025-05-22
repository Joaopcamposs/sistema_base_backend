from pydantic import UUID4

from contextos_de_negocio.dominio.entidades.registro_de_servico import (
    RegistroDeServicoEntidade,
)
from contextos_de_negocio.barramento.unidade_de_trabalho import UnidadeDeTrabalho
from libs.ddd.adaptadores.visualizadores.visualizadores import Filtros


async def listar_registros_por_id_e_codigo(
    unidade_de_trabalho: UnidadeDeTrabalho,
    id: UUID4 | None = None,
    codigo: str | None = None,
) -> list[RegistroDeServicoEntidade]:
    from contextos_de_negocio import Dominio, RegistroDeServicoRepoConsulta

    filtros = Filtros(
        {
            "id": id,
            "codigo": codigo,
        }
    )

    async with unidade_de_trabalho(Dominio.registro_de_servico) as uow:
        repo_consulta: RegistroDeServicoRepoConsulta = uow.view_repo

        registros = await repo_consulta.consultar_por_filtros(filtros=filtros)

    return registros
