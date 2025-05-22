from uuid import UUID

from contextos_de_negocio.dominio.comandos.cliente import (
    CadastrarCliente,
    AtualizarCliente,
    RemoverCliente,
)
from contextos_de_negocio.barramento.unidade_de_trabalho import UnidadeDeTrabalho
from libs.ddd.adaptadores.visualizadores.visualizadores import Filtros


async def cadastrar_cliente(
    comando: CadastrarCliente, unidade_de_trabalho: UnidadeDeTrabalho
) -> UUID:
    from contextos_de_negocio import Dominio, ClienteRepoDominio

    async with unidade_de_trabalho(Dominio.cliente) as uow:
        repo_dominio: ClienteRepoDominio = uow.domain_repo

        novo_cliente = await repo_dominio.gerar_agregado_para_cadastro(
            nome=comando.nome,
            cpf=comando.cpf,
            telefone=comando.telefone,
            telefone_2=comando.telefone_2,
            email=comando.email,
            endereco=comando.endereco,
        )
        novo_cliente.cadastrar(
            usuario=uow.usuario,
        )

        await repo_dominio.adicionar(
            cliente=novo_cliente,
        )
        await uow.commit()

    return novo_cliente.id


async def atualizar_cliente(
    comando: AtualizarCliente, unidade_de_trabalho: UnidadeDeTrabalho
) -> UUID:
    from contextos_de_negocio import Dominio, ClienteRepoDominio

    async with unidade_de_trabalho(Dominio.cliente) as uow:
        repo_dominio: ClienteRepoDominio = uow.domain_repo

        filtros = Filtros(
            {
                "id": comando.id,
                "cpf": comando.cpf_busca,
            }
        )
        cliente = await repo_dominio.consultar_um_por_filtros(filtros=filtros)
        cliente.atualizar(
            nome=comando.nome,
            cpf=comando.cpf,
            telefone=comando.telefone,
            telefone_2=comando.telefone_2,
            email=comando.email,
            endereco=comando.endereco,
            usuario=uow.usuario,
        )

        await repo_dominio.adicionar(
            cliente=cliente,
        )
        await uow.commit()

    return cliente.id


async def remover_cliente(
    comando: RemoverCliente, unidade_de_trabalho: UnidadeDeTrabalho
) -> UUID:
    from contextos_de_negocio import Dominio, ClienteRepoDominio

    async with unidade_de_trabalho(Dominio.cliente) as uow:
        repo_dominio: ClienteRepoDominio = uow.domain_repo

        filtros = Filtros(
            {
                "id": comando.id,
                "cpf": comando.cpf,
            }
        )
        cliente = await repo_dominio.consultar_um_por_filtros(filtros=filtros)
        cliente.remover(usuario=uow.usuario)

        await repo_dominio.remover(
            cliente=cliente,
        )
        await uow.commit()

    return cliente.id
