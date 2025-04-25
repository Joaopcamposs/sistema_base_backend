from uuid import UUID, uuid4

from contextos_de_negocio.barramento import bootstrap
from contextos_de_negocio.dominio.comandos.empresa import CadastrarEmpresa
from contextos_de_negocio.dominio.entidades.usuario import UsuarioEntidade
from contextos_de_negocio.unidade_de_trabalho import UnidadeDeTrabalho
from infra.banco_de_dados import (
    criar_schema_e_tabelas,
    listar_schemas_existentes,
    excluir_schema,
)
from libs.ddd.adaptadores.visualizadores.visualizadores import Filtros
from libs.ddd.barramento import logger
from libs.utils.constantes import (
    SENHA_PRIMEIRO_USUARIO,
    EMAIL_PRIMEIRO_USUARIO,
    CPF_PRIMEIRO_USUARIO,
)


def gerar_usuario_fake_primeiro_cadastro(id_empresa: UUID) -> UsuarioEntidade:
    usuario_fake = UsuarioEntidade(
        empresa=id_empresa,
        nome="Usuario Fake",
        email=EMAIL_PRIMEIRO_USUARIO,
        cpf=CPF_PRIMEIRO_USUARIO,
        _senha_hash=SENHA_PRIMEIRO_USUARIO,
        ativo=True,
        adm=True,
        permissoes=[],
        id=None,
    )
    return usuario_fake


async def criar_primeira_empresa(id_empresa: UUID) -> None:
    from contextos_de_negocio import Dominio, EmpresaRepoConsulta

    usuario_fake = gerar_usuario_fake_primeiro_cadastro(id_empresa)
    unidade_de_trabalho = UnidadeDeTrabalho(usuario=usuario_fake)

    async with unidade_de_trabalho(Dominio.empresa) as uow:
        repo_consulta: EmpresaRepoConsulta = uow.view_repo
        empresas = await repo_consulta.consultar_por_filtros(Filtros({}))
        if empresas:
            return None

    bus = bootstrap(uow=unidade_de_trabalho)
    await bus.handle(
        CadastrarEmpresa(
            id=id_empresa,
            razao_social="JP ADM",
            nome_responsavel="João Campos",
            email=EMAIL_PRIMEIRO_USUARIO,
            senha=SENHA_PRIMEIRO_USUARIO,
            cpf=CPF_PRIMEIRO_USUARIO,
            ativo=True,
            deve_criar_usuario=True,
        )
    )
    return None


async def criar_primeira_empresa_e_usuario() -> None:
    schemas = await listar_schemas_existentes()
    # verificar se algum schema é um uuid valido
    for schema in schemas:
        try:
            UUID(schema)
            return
        except ValueError:
            pass

    id_empresa = uuid4()
    await criar_schema_e_tabelas(str(id_empresa))

    # criar empresa
    try:
        await criar_primeira_empresa(id_empresa)
    except Exception as erro:
        await excluir_schema(str(id_empresa))
        logger.error(f"Erro ao criar empresa. O schema {id_empresa} foi dropado", erro)
        raise erro
