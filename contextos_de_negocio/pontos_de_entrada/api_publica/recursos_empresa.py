from http import HTTPStatus
from uuid import uuid4

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
from infra.banco_de_dados import (
    excluir_schema,
    criar_schema_e_tabelas,
    validar_email_da_empresa,
)
from libs.ddd.barramento import logger
from libs.utils.constantes import CHAVE_SECRETA

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
    if novo_empresa.chave_secreta != CHAVE_SECRETA:
        raise ValueError("Chave secreta inválida")

    id_empresa = uuid4()

    try:
        await validar_email_da_empresa(novo_empresa.email)

        await criar_schema_e_tabelas(str(id_empresa))

        bus = bootstrap(
            usuario=current_user.get(),
            schema=str(id_empresa),
            eh_criacao_de_nova_empresa=True,
        )

        comando = CadastrarEmpresa(
            razao_social=novo_empresa.razao_social,
            nome_responsavel=novo_empresa.nome_responsavel,
            ativo=novo_empresa.ativo,
            cpf=novo_empresa.cpf,
            email=novo_empresa.email,
            senha=novo_empresa.senha,
            cnpj=novo_empresa.cnpj,
            nome_fantasia=novo_empresa.nome_fantasia,
            id=id_empresa,
            deve_criar_usuario=novo_empresa.deve_criar_usuario,
        )
        retorno = await bus.handle(comando)

        return JSONResponse(status_code=HTTPStatus.CREATED, content=str(retorno))
    except Exception as erro:
        await excluir_schema(str(id_empresa))
        logger.error(f"Erro ao criar empresa. O schema {id_empresa} foi dropado", erro)
        raise erro


@router_empresa.put("/empresa", response_model=LerEmpresaSchema)
async def atualizar(
    empresa_atualizado: AtualizarEmpresaSchema,
    id: UUID4 | None = None,
    email: str | None = None,
):
    bus = bootstrap(usuario=current_user.get())

    comando = AtualizarEmpresa(**empresa_atualizado.__dict__, id=id, email_antigo=email)
    retorno = await bus.handle(comando)

    return JSONResponse(status_code=HTTPStatus.OK, content=str(retorno))


@router_empresa.delete("/empresa")
async def remover(
    id: UUID4 | None = None,
    email: str | None = None,
):
    bus = bootstrap(usuario=current_user.get())

    comando = RemoverEmpresa(id=id, email=email)
    retorno = await bus.handle(comando)

    return JSONResponse(status_code=HTTPStatus.OK, content=str(retorno))
