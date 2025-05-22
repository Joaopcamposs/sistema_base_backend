from pydantic import UUID4

from contextos_de_negocio.dominio.entidades.cliente import ClienteEntidade
from contextos_de_negocio.barramento.unidade_de_trabalho import UnidadeDeTrabalho
from libs.ddd.adaptadores.visualizadores.visualizadores import Filtros
from libs.utils.tipos_basicos import CPF


async def listar_clientes_por_id_e_cpf(
    unidade_de_trabalho: UnidadeDeTrabalho,
    id: UUID4 | None = None,
    cpf: str | None = None,
) -> list[ClienteEntidade]:
    from contextos_de_negocio import Dominio, ClienteRepoConsulta

    filtros = Filtros(
        {
            "id": id,
            "cpf": CPF(cpf) if cpf else None,
        }
    )

    async with unidade_de_trabalho(Dominio.cliente) as uow:
        repo_consulta: ClienteRepoConsulta = uow.view_repo

        clientes = await repo_consulta.consultar_por_filtros(filtros=filtros)

    return clientes
