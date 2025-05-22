from http import HTTPStatus

from fastapi import APIRouter, Depends
from pydantic import UUID4
from starlette.responses import JSONResponse

from contextos_de_negocio.adaptadores.visualizadores.cliente import (
    listar_clientes_por_id_e_cpf,
)
from contextos_de_negocio.barramento import bootstrap
from contextos_de_negocio.dominio.comandos.cliente import (
    CadastrarCliente,
    AtualizarCliente,
    RemoverCliente,
)
from contextos_de_negocio.dominio.entidades.cliente import ClienteEntidade
from contextos_de_negocio.dominio.excecoes import ClienteNaoEncontrado
from contextos_de_negocio.pontos_de_entrada.schemas.cliente import (
    CadastrarClienteSchema,
    LerClienteSchema,
    AtualizarClienteSchema,
)
from contextos_de_negocio.servicos.executores.seguranca import (
    get_current_user,
    current_user,
)
from contextos_de_negocio.barramento.unidade_de_trabalho import UnidadeDeTrabalho

router_cliente = APIRouter(
    prefix="/api/v1", tags=["Clientes"], dependencies=[Depends(get_current_user)]
)


@router_cliente.get("/clientes", response_model=list[LerClienteSchema])
async def listar(
    id: UUID4 | None = None, cpf: str | None = None
) -> list[ClienteEntidade]:
    unidade_de_trabalho: UnidadeDeTrabalho = UnidadeDeTrabalho(usuario=current_user.get())

    clientes = await listar_clientes_por_id_e_cpf(
        unidade_de_trabalho=unidade_de_trabalho, id=id, cpf=cpf
    )

    if not clientes:
        raise ClienteNaoEncontrado

    return clientes


@router_cliente.post("/cliente")
async def cadastrar(
    novo_cliente: CadastrarClienteSchema,
) -> JSONResponse:
    bus = bootstrap(usuario=current_user.get())

    comando = CadastrarCliente(**novo_cliente.__dict__)
    retorno = await bus.handle(comando)

    return JSONResponse(status_code=HTTPStatus.CREATED, content=str(retorno))


@router_cliente.put("/cliente", response_model=LerClienteSchema)
async def atualizar(
    cliente_atualizado: AtualizarClienteSchema,
    id: UUID4 | None = None,
    cpf: str | None = None,
) -> JSONResponse:
    bus = bootstrap(usuario=current_user.get())

    comando = AtualizarCliente(**cliente_atualizado.__dict__, id=id, cpf_busca=cpf)
    retorno = await bus.handle(comando)

    return JSONResponse(status_code=HTTPStatus.OK, content=str(retorno))


@router_cliente.delete("/cliente")
async def remover(id: UUID4 | None = None, cpf: str | None = None) -> JSONResponse:
    bus = bootstrap(usuario=current_user.get())

    comando = RemoverCliente(id=id, cpf=cpf)
    retorno = await bus.handle(comando)

    return JSONResponse(status_code=HTTPStatus.OK, content=str(retorno))
