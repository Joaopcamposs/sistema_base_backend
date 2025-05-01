from pydantic import UUID4

from contextos_de_negocio.dominio.entidades.usuario import UsuarioEntidade
from contextos_de_negocio.barramento.unidade_de_trabalho import UnidadeDeTrabalho
from libs.ddd.adaptadores.visualizadores.visualizadores import Filtros
from libs.utils.tipos_basicos import Email


async def listar_usuarios_por_id_e_email(
    unidade_de_trabalho: UnidadeDeTrabalho,
    id: UUID4 | None = None,
    email: str | None = None,
) -> list[UsuarioEntidade]:
    from contextos_de_negocio import Dominio, UsuarioRepoConsulta

    filtros = Filtros(
        {
            "id": id,
            "email": Email(email),
        }
    )

    async with unidade_de_trabalho(Dominio.usuario) as uow:
        repo_consulta: UsuarioRepoConsulta = uow.view_repo

        usuarios = await repo_consulta.consultar_por_filtros(filtros=filtros)

    return usuarios
