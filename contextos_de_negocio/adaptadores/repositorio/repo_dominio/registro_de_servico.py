from abc import abstractmethod
from datetime import datetime
from decimal import Decimal

from sqlalchemy import select, insert, update, delete
from uuid import UUID

from contextos_de_negocio.adaptadores.orm.declarativo import SessaoDeServicosDB, ServicoDB
from contextos_de_negocio.adaptadores.orm.declarativo.registro_de_servico import (
    RegistroDeServicoDB,
)
from contextos_de_negocio.dominio.agregados.registro_de_servico import RegistroDeServico
from contextos_de_negocio.dominio.excecoes import (
    RegistroDeServicoNaoEncontrado,
    SessaoDeServicosNaoEncontrado,
    ServicoNaoEncontrado,
)
from libs.ddd.adaptadores.repositorio.repositorio import RepositorioDominio
from libs.utils.tipos_basicos import TipoDeOperacao


class RegistroDeServicoRepoDominioAbstrato(RepositorioDominio):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.seen: set[RegistroDeServico] = set()

    async def adicionar(self, registro: RegistroDeServico) -> None:
        self.seen.add(registro)
        await self._adicionar(registro)

    @abstractmethod
    async def _adicionar(self, registro: RegistroDeServico) -> None:
        raise NotImplementedError

    async def remover(self, registro: RegistroDeServico) -> None:
        await self._remover(registro)

    @abstractmethod
    async def _remover(self, registro: RegistroDeServico) -> None:
        raise NotImplementedError

    @abstractmethod
    async def consultar_um_por_id(self, id: UUID) -> RegistroDeServico:
        raise NotImplementedError()


class RegistroDeServicoRepoDominio(RegistroDeServicoRepoDominioAbstrato):
    async def gerar_agregado_para_cadastro(
        self,
        codigo_sessao_de_servicos: int,
        codigo_servico: str,
        valor: Decimal,
        data_realizacao: datetime,
    ) -> RegistroDeServico:
        async with self.session as session:
            sessao_de_servicos = (
                await session.execute(
                    select(SessaoDeServicosDB).where(
                        SessaoDeServicosDB.codigo == codigo_sessao_de_servicos,
                        SessaoDeServicosDB.deletado_em.is_(None),
                    )
                )
            ).scalar_one_or_none()
            if not sessao_de_servicos:
                raise SessaoDeServicosNaoEncontrado

            servico = (
                await session.execute(
                    select(ServicoDB).where(
                        ServicoDB.codigo == codigo_servico,
                        ServicoDB.deletado_em.is_(None),
                    )
                )
            ).scalar_one_or_none()
            if not servico:
                raise ServicoNaoEncontrado

            return RegistroDeServico.retornar_agregado_para_cadastro(
                id_sessao_de_servicos=sessao_de_servicos.id,
                codigo_sessao_de_servicos=codigo_sessao_de_servicos,
                id_servico=servico.id,
                codigo_servico=codigo_servico,
                nome=servico.nome,
                valor=valor or servico.valor,
                descricao=servico.descricao,
                data_realizacao=data_realizacao,
            )

    async def consultar_um_por_id(self, id: UUID) -> RegistroDeServico:
        async with self.session as session:
            registro = (
                await session.execute(
                    select(RegistroDeServicoDB).where(
                        RegistroDeServicoDB.id == id,
                        RegistroDeServicoDB.deletado_em.is_(None),
                    )
                )
            ).scalar_one_or_none()
            if not registro:
                raise RegistroDeServicoNaoEncontrado

            return RegistroDeServico(
                id=registro.id,
                id_sessao_de_servicos=registro.id_sessao_de_servicos,
                codigo_sessao_de_servicos=registro.codigo_sessao_de_servicos,
                id_servico=registro.id_servico,
                codigo_servico=registro.codigo_servico,
                nome=registro.nome,
                valor=registro.valor,
                descricao=registro.descricao,
                data_realizacao=registro.data_realizacao,
            )

    async def _adicionar(self, registro: RegistroDeServico) -> None:
        dados = {
            "id": registro.id,
            "id_sessao_de_servicos": registro.id_sessao_de_servicos,
            "codigo_sessao_de_servicos": registro.codigo_sessao_de_servicos,
            "id_servico": registro.id_servico,
            "codigo_servico": registro.codigo_servico,
            "nome": registro.nome,
            "valor": registro.valor,
            "descricao": registro.descricao,
            "data_realizacao": registro.data_realizacao,
            "criado_por": registro.criado_por,
            "criado_em": registro.criado_em,
            "modificado_por": registro.modificado_por,
            "ultima_modificacao_em": registro.ultima_modificacao_em,
            "deletado_por": registro.deletado_por,
            "deletado_em": registro.deletado_em,
        }

        match registro._tipo_de_operacao:
            case TipoDeOperacao.INSERCAO:
                operacao = insert(RegistroDeServicoDB).values(dados)
            case TipoDeOperacao.ATUALIZACAO:
                operacao = (
                    update(RegistroDeServicoDB)
                    .where(RegistroDeServicoDB.id == registro.id)
                    .values(dados)
                )
            case _:
                raise ValueError(
                    "Tipo de operação não suportado para o repositório de domínio."
                )

        await self.session.execute(operacao)

    async def _remover(self, registro: RegistroDeServico) -> None:
        if registro._usa_soft_delete:
            dados = {
                "modificado_por": registro.modificado_por,
                "ultima_modificacao_em": registro.ultima_modificacao_em,
                "deletado_por": registro.deletado_por,
                "deletado_em": registro.deletado_em,
            }

            operacao = (
                update(RegistroDeServicoDB)
                .where(RegistroDeServicoDB.id == registro.id)
                .values(dados)
            )
        else:
            operacao = delete(RegistroDeServicoDB).where(
                RegistroDeServicoDB.id == registro.id
            )

        await self.session.execute(operacao)
