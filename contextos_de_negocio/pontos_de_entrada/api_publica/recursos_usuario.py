from http import HTTPStatus

from fastapi import APIRouter
from pydantic import UUID4
from starlette.responses import JSONResponse

from contextos_de_negocio.adaptadores.visualizadores.usuario import (
    listar_usuarios_por_id_e_email,
)
from contextos_de_negocio.barramento import bootstrap
from contextos_de_negocio.dominio.comandos.usuario import (
    CadastrarUsuario,
    AtualizarUsuario,
    RemoverUsuario,
)
from contextos_de_negocio.dominio.excecoes import UsuarioNaoEncontrado
from contextos_de_negocio.pontos_de_entrada.schemas.usuario import (
    CadastrarUsuarioSchema,
    LerUsuarioSchema,
    AtualizarUsuarioSchema,
)
from contextos_de_negocio.unidade_de_trabalho import UnidadeDeTrabalho
from infra.banco_de_dados import DEFAULT_SQL_SESSION_FACTORY

router_usuario = APIRouter(prefix="/api/v1", tags=["Usuários"])


async def obter_usuario_padrao_temporariamente() -> None:
    from contextos_de_negocio import UsuarioRepoConsulta

    async with DEFAULT_SQL_SESSION_FACTORY(somente_leitura=True) as session:
        repo = UsuarioRepoConsulta(session=session)
        usuario = await repo.consultar_um_por_email(email="joao")

    return usuario


@router_usuario.get("/usuarios", response_model=list[LerUsuarioSchema])
async def listar(id: UUID4 | None = None, email: str | None = None):
    usuario = await obter_usuario_padrao_temporariamente()

    unidade_de_trabalho = UnidadeDeTrabalho(usuario=usuario)

    usuarios = await listar_usuarios_por_id_e_email(
        unidade_de_trabalho=unidade_de_trabalho, id=id, email=email
    )

    if not usuarios:
        raise UsuarioNaoEncontrado

    return usuarios


@router_usuario.post("/usuario")
async def cadastrar(
    novo_usuario: CadastrarUsuarioSchema,
):
    usuario = await obter_usuario_padrao_temporariamente()

    bus = bootstrap(usuario=usuario)

    comando = CadastrarUsuario(**novo_usuario.__dict__)
    retorno = await bus.handle(comando)

    return JSONResponse(status_code=HTTPStatus.CREATED, content=str(retorno))


@router_usuario.put("/usuario", response_model=LerUsuarioSchema)
async def atualizar(
    usuario_atualizado: AtualizarUsuarioSchema,
    id: UUID4 | None = None,
    email: str | None = None,
):
    usuario = await obter_usuario_padrao_temporariamente()

    bus = bootstrap(usuario=usuario)

    comando = AtualizarUsuario(**usuario_atualizado.__dict__, id=id, email_antigo=email)
    retorno = await bus.handle(comando)

    return JSONResponse(status_code=HTTPStatus.OK, content=str(retorno))


@router_usuario.delete("/usuario")
async def remover(id: UUID4 | None = None, email: str | None = None):
    usuario = await obter_usuario_padrao_temporariamente()

    bus = bootstrap(usuario=usuario)

    comando = RemoverUsuario(id=id, email=email)
    retorno = await bus.handle(comando)

    return JSONResponse(status_code=HTTPStatus.OK, content=str(retorno))
