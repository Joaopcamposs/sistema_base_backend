from uuid import UUID

from contextos_de_negocio.dominio.comandos.usuario import (
    CadastrarUsuario,
    AtualizarUsuario,
    RemoverUsuario,
)
from contextos_de_negocio.unidade_de_trabalho import UnidadeDeTrabalho
from libs.ddd.adaptadores.visualizadores.visualizadores import Filtros


async def cadastrar_usuario(
    comando: CadastrarUsuario, unidade_de_trabalho: UnidadeDeTrabalho
) -> UUID:
    from contextos_de_negocio import Dominio, UsuarioRepoDominio

    async with unidade_de_trabalho(Dominio.usuario) as uow:
        repo_dominio: UsuarioRepoDominio = uow.domain_repo

        novo_usuario = await repo_dominio.gerar_agregado_para_cadastro(
            empresa=comando.empresa,
            nome=comando.nome,
            email=comando.email,
            cpf=comando.cpf,
            senha=comando.senha,
            adm=comando.adm,
            ativo=comando.ativo,
            permissoes=comando.permissoes,
        )
        novo_usuario.cadastrar(
            usuario=uow.usuario,
        )

        await repo_dominio.adicionar(
            usuario=novo_usuario,
        )
        await uow.commit()

    return novo_usuario.id


async def atualizar_usuario(
    comando: AtualizarUsuario, unidade_de_trabalho: UnidadeDeTrabalho
) -> UUID:
    from contextos_de_negocio import Dominio, UsuarioRepoDominio

    async with unidade_de_trabalho(Dominio.usuario) as uow:
        repo_dominio: UsuarioRepoDominio = uow.repo_escrita

        filtros = Filtros(
            {
                "id": comando.id,
                "email": comando.email,
            }
        )
        usuario = await repo_dominio.consultar_um_por_filtros(filtros=filtros)
        usuario.atualizar(
            nome=comando.nome,
            email=comando.email,
            cpf=comando.cpf,
            senha=comando.senha,
            adm=comando.adm,
            ativo=comando.ativo,
            permissoes=comando.permissoes,
            usuario=uow.usuario,
        )

        await repo_dominio.adicionar(
            usuario=usuario,
        )
        await uow.commit()

    return usuario.id


async def remover_usuario(
    comando: RemoverUsuario, unidade_de_trabalho: UnidadeDeTrabalho
) -> UUID:
    from contextos_de_negocio import Dominio, UsuarioRepoDominio

    async with unidade_de_trabalho(Dominio.usuario) as uow:
        repo_dominio: UsuarioRepoDominio = uow.repo_escrita

        filtros = Filtros(
            {
                "id": comando.id,
                "email": comando.email,
            }
        )
        usuario = await repo_dominio.consultar_um_por_filtros(filtros=filtros)
        usuario.remover(usuario=uow.usuario)

        await repo_dominio.remover(
            usuario=usuario,
        )
        await uow.commit()

    return usuario.id
