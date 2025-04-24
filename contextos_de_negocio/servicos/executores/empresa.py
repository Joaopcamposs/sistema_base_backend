from uuid import UUID

from contextos_de_negocio.dominio.comandos.empresa import (
    CadastrarEmpresa,
    AtualizarEmpresa,
    RemoverEmpresa,
)
from contextos_de_negocio.unidade_de_trabalho import UnidadeDeTrabalho
from libs.ddd.adaptadores.visualizadores.visualizadores import Filtros


async def cadastrar_empresa(
    comando: CadastrarEmpresa, unidade_de_trabalho: UnidadeDeTrabalho
) -> UUID:
    from contextos_de_negocio import Dominio, EmpresaRepoDominio

    async with unidade_de_trabalho(Dominio.empresa) as uow:
        repo_dominio: EmpresaRepoDominio = uow.domain_repo

        nova_empresa = await repo_dominio.gerar_agregado_para_cadastro(
            razao_social=comando.razao_social,
            nome_fantasia=comando.nome_fantasia,
            nome_responsavel=comando.nome_responsavel,
            email=comando.email,
            cpf=comando.cpf,
            cnpj=comando.cnpj,
            ativo=comando.ativo,
        )
        nova_empresa.cadastrar(
            usuario=uow.usuario,
        )

        await repo_dominio.adicionar(
            empresa=nova_empresa,
        )
        await uow.commit()

    return nova_empresa.id


async def atualizar_empresa(
    comando: AtualizarEmpresa, unidade_de_trabalho: UnidadeDeTrabalho
) -> UUID:
    from contextos_de_negocio import Dominio, EmpresaRepoDominio

    async with unidade_de_trabalho(Dominio.empresa) as uow:
        repo_dominio: EmpresaRepoDominio = uow.domain_repo

        filtros = Filtros(
            {
                "id": comando.id,
            }
        )
        empresa = await repo_dominio.consultar_um_por_filtros(filtros=filtros)
        empresa.atualizar(
            razao_social=comando.razao_social,
            nome_fantasia=comando.nome_fantasia,
            nome_responsavel=comando.nome_responsavel,
            email=comando.email,
            cpf=comando.cpf,
            cnpj=comando.cnpj,
            ativo=comando.ativo,
            usuario=uow.usuario,
        )

        await repo_dominio.adicionar(
            empresa=empresa,
        )
        await uow.commit()

    return empresa.id


async def remover_empresa(
    comando: RemoverEmpresa, unidade_de_trabalho: UnidadeDeTrabalho
) -> UUID:
    from contextos_de_negocio import Dominio, EmpresaRepoDominio

    async with unidade_de_trabalho(Dominio.usuario) as uow:
        repo_dominio: EmpresaRepoDominio = uow.domain_repo

        filtros = Filtros(
            {
                "id": comando.id,
            }
        )
        empresa = await repo_dominio.consultar_um_por_filtros(filtros=filtros)
        empresa.remover(usuario=uow.usuario)

        await repo_dominio.remover(
            empresa=empresa,
        )
        await uow.commit()

    return empresa.id
