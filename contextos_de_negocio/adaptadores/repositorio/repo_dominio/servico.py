from abc import abstractmethod
from sqlalchemy import select, insert, update, delete

from contextos_de_negocio.adaptadores.orm.declarativo.servico import ServicoDB
from contextos_de_negocio.dominio.agregados.servico import Servico
from contextos_de_negocio.dominio.excecoes import (
    ServicoNaoEncontrado,
    ServicoJaCadastrado,
)
from libs.ddd.adaptadores.repositorio.repositorio import RepositorioDominio
from libs.ddd.adaptadores.visualizadores.visualizadores import Filtros
from libs.utils.constantes import NAO_DELETADO
from libs.utils.tipos_basicos import TipoDeOperacao


class ServicoRepoDominioAbstrato(RepositorioDominio):
    def __init__(self, *args, **kwargs):
        super(ServicoRepoDominioAbstrato, self).__init__(*args, **kwargs)
        self.seen: set[Servico] = set()

    async def adicionar(self, servico: Servico) -> None:
        self.seen.add(servico)
        await self._adicionar(servico)

    @abstractmethod
    async def _adicionar(self, servico: Servico) -> None:
        raise NotImplementedError

    async def remover(self, servico: Servico) -> None:
        await self._remover(servico)

    @abstractmethod
    async def _remover(self, servico: Servico) -> None:
        raise NotImplementedError

    @abstractmethod
    async def consultar_um_por_filtros(self, filtros: Filtros) -> Servico:
        raise NotImplementedError()


class ServicoRepoDominio(ServicoRepoDominioAbstrato):
    async def gerar_agregado_para_cadastro(
        self,
        codigo: str,
        nome: str,
        descricao: str,
        valor: float,
    ) -> Servico:
        async with self.session as session:
            servico_com_mesmo_codigo = (
                await session.execute(
                    select(ServicoDB).where(
                        ServicoDB.codigo == codigo, ServicoDB.deletado_em.is_(None)
                    )
                )
            ).scalar_one_or_none()
            if servico_com_mesmo_codigo:
                raise ServicoJaCadastrado

        return Servico.retornar_agregado_para_cadastro(
            codigo=codigo,
            nome=nome,
            descricao=descricao,
            valor=valor,
        )

    async def consultar_um_por_filtros(self, filtros: Filtros) -> Servico:
        async with self.session as session:
            servico = (
                await session.execute(
                    select(ServicoDB).filter_by(**filtros, **NAO_DELETADO)
                )
            ).scalar_one_or_none()
            if not servico:
                raise ServicoNaoEncontrado

            agregado = Servico(
                id=servico.id,
                codigo=servico.codigo,
                nome=servico.nome,
                descricao=servico.descricao,
                valor=servico.valor,
                criado_por=servico.criado_por,
                criado_em=servico.criado_em,
                ultima_modificacao_em=servico.ultima_modificacao_em,
                modificado_por=servico.modificado_por,
                deletado_em=servico.deletado_em,
                deletado_por=servico.deletado_por,
            )

        return agregado

    async def _adicionar(self, servico: Servico) -> None:
        dados = {
            "id": servico.id,
            "codigo": servico.codigo,
            "nome": servico.nome,
            "descricao": servico.descricao,
            "valor": servico.valor,
            "criado_por": servico.criado_por,
            "criado_em": servico.criado_em,
            "modificado_por": servico.modificado_por,
            "ultima_modificacao_em": servico.ultima_modificacao_em,
            "deletado_por": servico.deletado_por,
            "deletado_em": servico.deletado_em,
        }

        match servico._tipo_de_operacao:
            case TipoDeOperacao.INSERCAO:
                operacao = insert(ServicoDB).values(dados)
            case TipoDeOperacao.ATUALIZACAO:
                operacao = (
                    update(ServicoDB).where(ServicoDB.id == servico.id).values(dados)
                )
            case _:
                raise ValueError(
                    "Tipo de operação não suportado para o repositório de domínio."
                )

        await self.session.execute(operacao)

    async def _remover(self, servico: Servico) -> None:
        if servico._usa_soft_delete:
            dados = {
                "modificado_por": servico.modificado_por,
                "ultima_modificacao_em": servico.ultima_modificacao_em,
                "deletado_por": servico.deletado_por,
                "deletado_em": servico.deletado_em,
            }

            operacao = update(ServicoDB).where(ServicoDB.id == servico.id).values(dados)
        else:
            operacao = delete(ServicoDB).where(ServicoDB.id == servico.id)

        await self.session.execute(operacao)
