from http import HTTPStatus

from fastapi import APIRouter, Depends
from pydantic import UUID4
from starlette.responses import JSONResponse

from contextos_de_negocio.adaptadores.visualizadores.empresa import listar_empresas_por_id
from contextos_de_negocio.barramento import bootstrap
from contextos_de_negocio.dominio.comandos.empresa import (
    CadastrarEmpresa,
    AtualizarEmpresa,
    RemoverEmpresa,
)
from contextos_de_negocio.dominio.excecoes import EmpresaNaoEncontrada
from contextos_de_negocio.pontos_de_entrada.schemas.empresa import (
    LerEmpresaSchema,
    CadastrarEmpresaSchema,
    AtualizarEmpresaSchema,
)
from contextos_de_negocio.servicos.executores.seguranca import (
    get_current_user,
    current_user,
)
from contextos_de_negocio.unidade_de_trabalho import UnidadeDeTrabalho

router_empresa = APIRouter(
    prefix="/api/v1", tags=["Empresas"], dependencies=[Depends(get_current_user)]
)


@router_empresa.get("/empresas", response_model=list[LerEmpresaSchema])
async def listar(id: UUID4 | None = None):
    unidade_de_trabalho = UnidadeDeTrabalho(usuario=current_user.get())

    empresas = await listar_empresas_por_id(
        unidade_de_trabalho=unidade_de_trabalho, id=id
    )

    if not empresas:
        raise EmpresaNaoEncontrada

    return empresas


@router_empresa.post("/empresa")
async def cadastrar(
    novo_empresa: CadastrarEmpresaSchema,
):
    bus = bootstrap(usuario=current_user.get())

    comando = CadastrarEmpresa(**novo_empresa.__dict__)
    retorno = await bus.handle(comando)

    return JSONResponse(status_code=HTTPStatus.CREATED, content=str(retorno))


@router_empresa.put("/empresa", response_model=LerEmpresaSchema)
async def atualizar(
    empresa_atualizado: AtualizarEmpresaSchema,
    id: UUID4 | None = None,
):
    bus = bootstrap(usuario=current_user.get())

    comando = AtualizarEmpresa(**empresa_atualizado.__dict__, id=id)
    retorno = await bus.handle(comando)

    return JSONResponse(status_code=HTTPStatus.OK, content=str(retorno))


@router_empresa.delete("/empresa")
async def remover(id: UUID4 | None = None):
    bus = bootstrap(usuario=current_user.get())

    comando = RemoverEmpresa(id=id)
    retorno = await bus.handle(comando)

    return JSONResponse(status_code=HTTPStatus.OK, content=str(retorno))
