from uuid import UUID

from contextos_de_negocio.dominio.comandos.sessao_de_servicos import (
    CadastrarSessaoDeServicos,
    AtualizarSessaoDeServicos,
    RemoverSessaoDeServicos,
)
from contextos_de_negocio.barramento.unidade_de_trabalho import UnidadeDeTrabalho
from libs.ddd.adaptadores.visualizadores.visualizadores import Filtros


async def cadastrar_sessao_de_servicos(
    comando: CadastrarSessaoDeServicos, unidade_de_trabalho: UnidadeDeTrabalho
) -> UUID:
    from contextos_de_negocio import Dominio, SessaoDeServicosRepoDominio

    async with unidade_de_trabalho(Dominio.sessao_de_servicos) as uow:
        repo_dominio: SessaoDeServicosRepoDominio = uow.domain_repo

        nova_sessao = await repo_dominio.gerar_agregado_para_cadastro(
            cpf_do_cliente=comando.cpf_do_cliente,
            nome_do_cliente=comando.nome_do_cliente,
            data_inicio_da_realizacao=comando.data_inicio_da_realizacao,
            data_final_da_realizacao=comando.data_final_da_realizacao,
            valor_total=comando.valor_total,
            valor_desconto=comando.valor_desconto,
            valor_pago=comando.valor_pago,
            valor_restante=comando.valor_restante,
            forma_de_pagamento=comando.forma_de_pagamento,
            observacoes=comando.observacoes,
            registros=comando.registros,
        )
        nova_sessao.cadastrar(
            usuario=uow.usuario,
        )

        await repo_dominio.adicionar(
            sessao=nova_sessao,
        )
        await uow.commit()

    return nova_sessao.id


async def atualizar_sessao_de_servicos(
    comando: AtualizarSessaoDeServicos, unidade_de_trabalho: UnidadeDeTrabalho
) -> UUID:
    from contextos_de_negocio import Dominio, SessaoDeServicosRepoDominio

    async with unidade_de_trabalho(Dominio.sessao_servicos) as uow:
        repo_dominio: SessaoDeServicosRepoDominio = uow.domain_repo

        filtros = Filtros(
            {
                "id": comando.id,
                "cliente_id": comando.cliente_id,
            }
        )
        sessao = await repo_dominio.consultar_um_por_filtros(filtros=filtros)
        sessao.atualizar(
            nome_do_cliente=comando.nome_do_cliente,
            data_inicio_da_realizacao=comando.data_inicio_da_realizacao,
            data_final_da_realizacao=comando.data_final_da_realizacao,
            valor_total=comando.valor_total,
            valor_desconto=comando.valor_desconto,
            valor_pago=comando.valor_pago,
            valor_restante=comando.valor_restante,
            forma_de_pagamento=comando.forma_de_pagamento,
            observacoes=comando.observacoes,
            registros=comando.registros,
            usuario=uow.usuario,
        )

        await repo_dominio.adicionar(
            sessao=sessao,
        )
        await uow.commit()

    return sessao.id


async def remover_sessao_de_servicos(
    comando: RemoverSessaoDeServicos, unidade_de_trabalho: UnidadeDeTrabalho
) -> UUID:
    from contextos_de_negocio import Dominio, SessaoDeServicosRepoDominio

    async with unidade_de_trabalho(Dominio.sessao_servicos) as uow:
        repo_dominio: SessaoDeServicosRepoDominio = uow.domain_repo

        filtros = Filtros(
            {
                "id": comando.id,
                "cliente_id": comando.cliente_id,
            }
        )
        sessao = await repo_dominio.consultar_um_por_filtros(filtros=filtros)
        sessao.remover(usuario=uow.usuario)

        await repo_dominio.remover(
            sessao=sessao,
        )
        await uow.commit()

    return sessao.id
