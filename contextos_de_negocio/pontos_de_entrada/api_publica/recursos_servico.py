from http import HTTPStatus

from fastapi import APIRouter, Depends
from pydantic import UUID4
from starlette.responses import JSONResponse

from contextos_de_negocio.adaptadores.visualizadores.servico import (
    listar_servicos_por_id_e_codigo,
)
from contextos_de_negocio.barramento import bootstrap
from contextos_de_negocio.dominio.comandos.servico import (
    CadastrarServico,
    AtualizarServico,
    RemoverServico,
)
from contextos_de_negocio.dominio.entidades.servico import ServicoEntidade
from contextos_de_negocio.dominio.excecoes import ServicoNaoEncontrado
from contextos_de_negocio.pontos_de_entrada.schemas.servico import (
    CadastrarServicoSchema,
    LerServicoSchema,
    AtualizarServicoSchema,
)
from contextos_de_negocio.servicos.executores.seguranca import (
    get_current_user,
    current_user,
)
from contextos_de_negocio.barramento.unidade_de_trabalho import UnidadeDeTrabalho

router_servico = APIRouter(
    prefix="/api/v1", tags=["Servicos"], dependencies=[Depends(get_current_user)]
)


@router_servico.get("/servicos", response_model=list[LerServicoSchema])
async def listar(
    id: UUID4 | None = None, codigo: str | None = None
) -> list[ServicoEntidade]:
    unidade_de_trabalho: UnidadeDeTrabalho = UnidadeDeTrabalho(usuario=current_user.get())

    servicos = await listar_servicos_por_id_e_codigo(
        unidade_de_trabalho=unidade_de_trabalho, id=id, codigo=codigo
    )

    if not servicos:
        raise ServicoNaoEncontrado

    return servicos


@router_servico.post("/servico")
async def cadastrar(
    novo_servico: CadastrarServicoSchema,
) -> JSONResponse:
    bus = bootstrap(usuario=current_user.get())

    comando = CadastrarServico(**novo_servico.__dict__)
    retorno = await bus.handle(comando)

    return JSONResponse(status_code=HTTPStatus.CREATED, content=str(retorno))


@router_servico.put("/servico", response_model=LerServicoSchema)
async def atualizar(
    servico_atualizado: AtualizarServicoSchema,
    id: UUID4 | None = None,
    codigo: str | None = None,
) -> JSONResponse:
    bus = bootstrap(usuario=current_user.get())

    comando = AtualizarServico(**servico_atualizado.__dict__, id=id, codigo_busca=codigo)
    retorno = await bus.handle(comando)

    return JSONResponse(status_code=HTTPStatus.OK, content=str(retorno))


@router_servico.delete("/servico")
async def remover(id: UUID4 | None = None, codigo: str | None = None) -> JSONResponse:
    bus = bootstrap(usuario=current_user.get())

    comando = RemoverServico(id=id, codigo=codigo)
    retorno = await bus.handle(comando)

    return JSONResponse(status_code=HTTPStatus.OK, content=str(retorno))
