from contextos_de_negocio.dominio.entidades.usuario import UsuarioEntidade
from contextos_de_negocio.unidade_de_trabalho import UnidadeDeTrabalho
from libs.ddd.adaptadores.visualizadores.visualizadores import Filtros


async def listar_usuarios_por_filtros(
    filtros: Filtros, unidade_de_trabalho: UnidadeDeTrabalho
) -> list[UsuarioEntidade]:
    from contextos_de_negocio import Dominio, UsuarioRepoConsulta

    async with unidade_de_trabalho(Dominio.usuario) as uow:
        repo_consulta: UsuarioRepoConsulta = uow.view_repo

        usuarios = await repo_consulta.consultar_por_filtros(filtros=filtros)

    return usuarios
