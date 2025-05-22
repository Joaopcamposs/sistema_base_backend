from uuid import UUID

from contextos_de_negocio.dominio.comandos.registro_de_servico import (
    CadastrarRegistroDeServico,
    AtualizarRegistroDeServico,
    RemoverRegistroDeServico,
)
from contextos_de_negocio.barramento.unidade_de_trabalho import UnidadeDeTrabalho
from libs.ddd.adaptadores.visualizadores.visualizadores import Filtros


async def cadastrar_registro_de_servico(
    comando: CadastrarRegistroDeServico, unidade_de_trabalho: UnidadeDeTrabalho
) -> UUID:
    from contextos_de_negocio import Dominio, RegistroDeServicoRepoDominio

    async with unidade_de_trabalho(Dominio.registro_de_servico) as uow:
        repo_dominio: RegistroDeServicoRepoDominio = uow.domain_repo

        novo_registro = await repo_dominio.gerar_agregado_para_cadastro(
            codigo_sessao_de_servicos=comando.codigo_sessao_de_servicos,
            codigo_servico=comando.codigo_servico,
            valor=comando.valor,
            data_realizacao=comando.data_realizacao,
        )
        novo_registro.cadastrar(
            usuario=uow.usuario,
        )

        await repo_dominio.adicionar(
            registro=novo_registro,
        )
        await uow.commit()

    return novo_registro.id


async def atualizar_registro_de_servico(
    comando: AtualizarRegistroDeServico, unidade_de_trabalho: UnidadeDeTrabalho
) -> UUID:
    from contextos_de_negocio import Dominio, RegistroDeServicoRepoDominio

    async with unidade_de_trabalho(Dominio.registro_servico) as uow:
        repo_dominio: RegistroDeServicoRepoDominio = uow.domain_repo

        filtros = Filtros(
            {
                "id": comando.id,
                "codigo": comando.codigo_busca,
            }
        )
        registro = await repo_dominio.consultar_um_por_filtros(filtros=filtros)
        registro.atualizar(
            codigo=comando.codigo,
            nome=comando.nome,
            valor=comando.valor,
            descricao=comando.descricao,
            data_realizacao=comando.data_realizacao,
            usuario=uow.usuario,
        )

        await repo_dominio.adicionar(
            registro=registro,
        )
        await uow.commit()

    return registro.id


async def remover_registro_de_servico(
    comando: RemoverRegistroDeServico, unidade_de_trabalho: UnidadeDeTrabalho
) -> UUID:
    from contextos_de_negocio import Dominio, RegistroDeServicoRepoDominio

    async with unidade_de_trabalho(Dominio.registro_servico) as uow:
        repo_dominio: RegistroDeServicoRepoDominio = uow.domain_repo

        filtros = Filtros(
            {
                "id": comando.id,
                "codigo": comando.codigo,
            }
        )
        registro = await repo_dominio.consultar_um_por_filtros(filtros=filtros)
        registro.remover(usuario=uow.usuario)

        await repo_dominio.remover(
            registro=registro,
        )
        await uow.commit()

    return registro.id
