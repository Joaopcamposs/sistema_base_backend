from http import HTTPStatus

from fastapi import APIRouter, Depends
from pydantic import UUID4
from starlette.responses import JSONResponse

from contextos_de_negocio.adaptadores.visualizadores.sessao_de_servicos import (
    listar_sessoes_por_id_e_cliente,
)
from contextos_de_negocio.barramento import bootstrap
from contextos_de_negocio.dominio.comandos.sessao_de_servicos import (
    CadastrarSessaoDeServicos,
    AtualizarSessaoDeServicos,
    RemoverSessaoDeServicos,
)
from contextos_de_negocio.dominio.entidades.sessao_de_servicos import (
    SessaoDeServicosEntidade,
)
from contextos_de_negocio.dominio.excecoes import SessaoDeServicosNaoEncontrado
from contextos_de_negocio.pontos_de_entrada.schemas.sessao_de_servicos import (
    CadastrarSessaoDeServicosSchema,
    LerSessaoDeServicosSchema,
    AtualizarSessaoDeServicosSchema,
)
from contextos_de_negocio.servicos.executores.seguranca import (
    get_current_user,
    current_user,
)
from contextos_de_negocio.barramento.unidade_de_trabalho import UnidadeDeTrabalho

router_sessao_de_servicos = APIRouter(
    prefix="/api/v1",
    tags=["Sessões de Serviços"],
    dependencies=[Depends(get_current_user)],
)


@router_sessao_de_servicos.get("/sessoes", response_model=list[LerSessaoDeServicosSchema])
async def listar(
    id: UUID4 | None = None, cpf_cliente: UUID4 | None = None
) -> list[SessaoDeServicosEntidade]:
    unidade_de_trabalho: UnidadeDeTrabalho = UnidadeDeTrabalho(usuario=current_user.get())

    sessoes = await listar_sessoes_por_id_e_cliente(
        unidade_de_trabalho=unidade_de_trabalho, id=id, cpf_cliente=cpf_cliente
    )

    if not sessoes:
        raise SessaoDeServicosNaoEncontrado

    return sessoes


@router_sessao_de_servicos.post("/sessao")
async def cadastrar(
    nova_sessao: CadastrarSessaoDeServicosSchema,
) -> JSONResponse:
    bus = bootstrap(usuario=current_user.get())

    comando = CadastrarSessaoDeServicos(**nova_sessao.__dict__)
    retorno = await bus.handle(comando)

    return JSONResponse(status_code=HTTPStatus.CREATED, content=str(retorno))


@router_sessao_de_servicos.put("/sessao", response_model=LerSessaoDeServicosSchema)
async def atualizar(
    sessao_atualizada: AtualizarSessaoDeServicosSchema,
    id: UUID4 | None = None,
    cliente_id: UUID4 | None = None,
) -> JSONResponse:
    bus = bootstrap(usuario=current_user.get())

    comando = AtualizarSessaoDeServicos(
        **sessao_atualizada.__dict__, id=id, cliente_id=cliente_id
    )
    retorno = await bus.handle(comando)

    return JSONResponse(status_code=HTTPStatus.OK, content=str(retorno))


@router_sessao_de_servicos.delete("/sessao")
async def remover(
    id: UUID4 | None = None, cliente_id: UUID4 | None = None
) -> JSONResponse:
    bus = bootstrap(usuario=current_user.get())

    comando = RemoverSessaoDeServicos(id=id, cliente_id=cliente_id)
    retorno = await bus.handle(comando)

    return JSONResponse(status_code=HTTPStatus.OK, content=str(retorno))
