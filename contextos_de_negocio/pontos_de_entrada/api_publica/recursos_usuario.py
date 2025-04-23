from fastapi import APIRouter
from pydantic import UUID4
from starlette.responses import JSONResponse

from contextos_de_negocio.adaptadores.visualizadores.usuario import (
    listar_usuarios_por_filtros,
)
from contextos_de_negocio.barramento import bootstrap
from contextos_de_negocio.dominio.comandos.usuario import CadastrarUsuario
from contextos_de_negocio.dominio.excecoes import UsuarioNaoEncontrado
from contextos_de_negocio.pontos_de_entrada.schemas.usuario import (
    CadastrarUsuarioSchema,
    LerUsuarioSchema,
)
from contextos_de_negocio.unidade_de_trabalho import UnidadeDeTrabalho
from infra.banco_de_dados import DEFAULT_SQL_SESSION_FACTORY
from libs.ddd.adaptadores.visualizadores.visualizadores import Filtros
from libs.utils.tipos_basicos import Email

router_usuario = APIRouter(prefix="/api/v1", tags=["Usuários"])


@router_usuario.get("/usuarios", response_model=list[LerUsuarioSchema])
async def listar(id: UUID4 | None = None, email: str | None = None):
    from contextos_de_negocio import UsuarioRepoConsulta

    session = await DEFAULT_SQL_SESSION_FACTORY(somente_leitura=True)
    repo = UsuarioRepoConsulta(session=session)
    usuario = await repo.consultar_um_por_email(email="joao")

    unidade_de_trabalho = UnidadeDeTrabalho(usuario=usuario)

    filtros = Filtros(
        {
            "id": id,
            "email": Email(email) if email else None,
        }
    )

    usuarios = await listar_usuarios_por_filtros(
        filtros=filtros, unidade_de_trabalho=unidade_de_trabalho
    )

    if not usuarios:
        raise UsuarioNaoEncontrado

    return usuarios


@router_usuario.post("/usuario")
async def cadastrar(
    novo_usuario: CadastrarUsuarioSchema,
):
    from contextos_de_negocio import UsuarioRepoConsulta

    session = await DEFAULT_SQL_SESSION_FACTORY(somente_leitura=True)
    repo = UsuarioRepoConsulta(session=session)
    usuario = await repo.consultar_um_por_email(email="joao")

    bus = bootstrap(usuario=usuario)

    comando = CadastrarUsuario(**novo_usuario.__dict__)
    retorno = await bus.handle(comando)

    return JSONResponse(status_code=201, content=str(retorno))
