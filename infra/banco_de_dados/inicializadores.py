from uuid import UUID, uuid4


from contextos_de_negocio.barramento import bootstrap
from contextos_de_negocio.dominio.comandos.empresa import CadastrarEmpresa
from contextos_de_negocio.dominio.entidades.usuario import UsuarioEntidade
from infra.banco_de_dados import (
    listar_schemas_existentes,
    excluir_schema,
)
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


async def criar_primeira_empresa_e_usuario() -> None:
    # verificar se algum schema é um uuid valido, se sim, não criar
    schemas = await listar_schemas_existentes()
    for schema in schemas:
        try:
            UUID(schema)
            return
        except ValueError:
            pass

    id_empresa = uuid4()
    usuario_fake = gerar_usuario_fake_primeiro_cadastro(id_empresa)
    bus = bootstrap(usuario=usuario_fake, schema=str(id_empresa), criar_schema=True)

    try:
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
    except Exception as erro:
        await excluir_schema(str(id_empresa))
        logger.error(
            f"Erro ao criar empresa. O schema {str(id_empresa)} foi dropado", erro
        )
        raise erro
