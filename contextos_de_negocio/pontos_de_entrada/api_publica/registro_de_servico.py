from http import HTTPStatus

from fastapi import APIRouter, Depends
from pydantic import UUID4
from starlette.responses import JSONResponse

from contextos_de_negocio.adaptadores.visualizadores.registro_de_servico import (
    listar_registros_por_id_e_codigo,
)
from contextos_de_negocio.barramento import bootstrap
from contextos_de_negocio.dominio.comandos.registro_de_servico import (
    CadastrarRegistroDeServico,
    AtualizarRegistroDeServico,
    RemoverRegistroDeServico,
)
from contextos_de_negocio.dominio.entidades.registro_de_servico import (
    RegistroDeServicoEntidade,
)
from contextos_de_negocio.dominio.excecoes import RegistroDeServicoNaoEncontrado
from contextos_de_negocio.pontos_de_entrada.schemas.registro_de_servico import (
    CadastrarRegistroDeServicoSchema,
    LerRegistroDeServicoSchema,
    AtualizarRegistroDeServicoSchema,
)
from contextos_de_negocio.servicos.executores.seguranca import (
    get_current_user,
    current_user,
)
from contextos_de_negocio.barramento.unidade_de_trabalho import UnidadeDeTrabalho

router_registro_de_servico = APIRouter(
    prefix="/api/v1",
    tags=["Registros de Serviço"],
    dependencies=[Depends(get_current_user)],
)


@router_registro_de_servico.get(
    "/registros", response_model=list[LerRegistroDeServicoSchema]
)
async def listar(
    id: UUID4 | None = None, codigo: str | None = None
) -> list[RegistroDeServicoEntidade]:
    unidade_de_trabalho: UnidadeDeTrabalho = UnidadeDeTrabalho(usuario=current_user.get())

    registros = await listar_registros_por_id_e_codigo(
        unidade_de_trabalho=unidade_de_trabalho, id=id, codigo=codigo
    )

    if not registros:
        raise RegistroDeServicoNaoEncontrado

    return registros


@router_registro_de_servico.post("/registro")
async def cadastrar(
    novo_registro: CadastrarRegistroDeServicoSchema,
) -> JSONResponse:
    bus = bootstrap(usuario=current_user.get())

    comando = CadastrarRegistroDeServico(**novo_registro.__dict__)
    retorno = await bus.handle(comando)

    return JSONResponse(status_code=HTTPStatus.CREATED, content=str(retorno))


@router_registro_de_servico.put("/registro", response_model=LerRegistroDeServicoSchema)
async def atualizar(
    registro_atualizado: AtualizarRegistroDeServicoSchema,
    id: UUID4 | None = None,
    codigo: str | None = None,
) -> JSONResponse:
    bus = bootstrap(usuario=current_user.get())

    comando = AtualizarRegistroDeServico(
        **registro_atualizado.__dict__, id=id, codigo_busca=codigo
    )
    retorno = await bus.handle(comando)

    return JSONResponse(status_code=HTTPStatus.OK, content=str(retorno))


@router_registro_de_servico.delete("/registro")
async def remover(id: UUID4 | None = None, codigo: str | None = None) -> JSONResponse:
    bus = bootstrap(usuario=current_user.get())

    comando = RemoverRegistroDeServico(id=id, codigo=codigo)
    retorno = await bus.handle(comando)

    return JSONResponse(status_code=HTTPStatus.OK, content=str(retorno))
