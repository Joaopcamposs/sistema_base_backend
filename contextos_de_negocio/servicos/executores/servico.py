from uuid import UUID

from contextos_de_negocio.dominio.comandos.servico import (
    CadastrarServico,
    AtualizarServico,
    RemoverServico,
)
from contextos_de_negocio.barramento.unidade_de_trabalho import UnidadeDeTrabalho
from libs.ddd.adaptadores.visualizadores.visualizadores import Filtros


async def cadastrar_servico(
    comando: CadastrarServico, unidade_de_trabalho: UnidadeDeTrabalho
) -> UUID:
    from contextos_de_negocio import Dominio, ServicoRepoDominio

    async with unidade_de_trabalho(Dominio.servico) as uow:
        repo_dominio: ServicoRepoDominio = uow.domain_repo

        novo_servico = await repo_dominio.gerar_agregado_para_cadastro(
            codigo=comando.codigo,
            nome=comando.nome,
            descricao=comando.descricao,
            valor=comando.valor,
        )
        novo_servico.cadastrar(
            usuario=uow.usuario,
        )

        await repo_dominio.adicionar(
            servico=novo_servico,
        )
        await uow.commit()

    return novo_servico.id


async def atualizar_servico(
    comando: AtualizarServico, unidade_de_trabalho: UnidadeDeTrabalho
) -> UUID:
    from contextos_de_negocio import Dominio, ServicoRepoDominio

    async with unidade_de_trabalho(Dominio.servico) as uow:
        repo_dominio: ServicoRepoDominio = uow.domain_repo

        filtros = Filtros(
            {
                "id": comando.id,
                "codigo": comando.codigo_busca,
            }
        )
        servico = await repo_dominio.consultar_um_por_filtros(filtros=filtros)
        servico.atualizar(
            codigo=comando.codigo,
            nome=comando.nome,
            descricao=comando.descricao,
            valor=comando.valor,
            usuario=uow.usuario,
        )

        await repo_dominio.adicionar(
            servico=servico,
        )
        await uow.commit()

    return servico.id


async def remover_servico(
    comando: RemoverServico, unidade_de_trabalho: UnidadeDeTrabalho
) -> UUID:
    from contextos_de_negocio import Dominio, ServicoRepoDominio

    async with unidade_de_trabalho(Dominio.servico) as uow:
        repo_dominio: ServicoRepoDominio = uow.domain_repo

        filtros = Filtros(
            {
                "id": comando.id,
                "codigo": comando.codigo,
            }
        )
        servico = await repo_dominio.consultar_um_por_filtros(filtros=filtros)
        servico.remover(usuario=uow.usuario)

        await repo_dominio.remover(
            servico=servico,
        )
        await uow.commit()

    return servico.id
