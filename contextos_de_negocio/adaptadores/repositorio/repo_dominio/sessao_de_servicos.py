from abc import abstractmethod
from datetime import datetime
from decimal import Decimal

from sqlalchemy import select, insert, update, delete
from uuid import UUID

from contextos_de_negocio.adaptadores.orm.declarativo import ClienteDB
from contextos_de_negocio.adaptadores.orm.declarativo.sessao_de_servicos import (
    SessaoDeServicosDB,
)
from contextos_de_negocio.dominio.agregados.registro_de_servico import RegistroDeServico
from contextos_de_negocio.dominio.agregados.sessao_de_servicos import SessaoDeServicos
from contextos_de_negocio.dominio.entidades.registro_de_servico import (
    RegistroDeServicoEntidade,
)
from contextos_de_negocio.dominio.excecoes import (
    SessaoDeServicosNaoEncontrado,
    ClienteNaoEncontrado,
)
from libs.ddd.adaptadores.repositorio.repositorio import RepositorioDominio
from libs.utils.tipos_basicos import TipoDeOperacao


class SessaoDeServicosRepoDominioAbstrato(RepositorioDominio):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.seen: set[SessaoDeServicos] = set()

    async def adicionar(self, sessao: SessaoDeServicos) -> None:
        self.seen.add(sessao)
        await self._adicionar(sessao)

    @abstractmethod
    async def _adicionar(self, sessao: SessaoDeServicos) -> None:
        raise NotImplementedError

    async def remover(self, sessao: SessaoDeServicos) -> None:
        await self._remover(sessao)

    @abstractmethod
    async def _remover(self, sessao: SessaoDeServicos) -> None:
        raise NotImplementedError

    @abstractmethod
    async def consultar_um_por_id(self, id: UUID) -> SessaoDeServicos:
        raise NotImplementedError()


class SessaoDeServicosRepoDominio(SessaoDeServicosRepoDominioAbstrato):
    async def gerar_agregado_para_cadastro(
        self,
        cpf_do_cliente: str,
        nome_do_cliente: str,
        data_inicio_da_realizacao: datetime,
        data_final_da_realizacao: datetime,
        valor_total: Decimal,
        valor_desconto: Decimal,
        valor_pago: Decimal,
        valor_restante: Decimal,
        forma_de_pagamento: str,
        observacoes: str,
        registros: list[RegistroDeServicoEntidade],
    ) -> SessaoDeServicos:
        async with self.session as session:
            cliente = (
                await session.execute(
                    select(ClienteDB).where(
                        ClienteDB.cpf == cpf_do_cliente, ClienteDB.deletado_em.is_(None)
                    )
                )
            ).scalar_one_or_none()
            if not cliente:
                raise ClienteNaoEncontrado

            agregados_de_registros = []
            if registros:
                agregados_de_registros = ...

            return SessaoDeServicos.retornar_agregado_para_cadastro(
                id_cliente=cliente.id,
                cpf_do_cliente=cpf_do_cliente,
                nome_do_cliente=nome_do_cliente,
                data_inicio_da_realizacao=data_inicio_da_realizacao,
                data_final_da_realizacao=data_final_da_realizacao,
                valor_total=valor_total,
                valor_desconto=valor_desconto,
                valor_pago=valor_pago,
                valor_restante=valor_restante,
                forma_de_pagamento=forma_de_pagamento,
                observacoes=observacoes,
                registros=agregados_de_registros,
            )

    async def consultar_um_por_id(self, id: UUID) -> SessaoDeServicos:
        async with self.session as session:
            sessao = (
                await session.execute(
                    select(SessaoDeServicosDB).where(
                        SessaoDeServicosDB.id == id,
                        SessaoDeServicosDB.deletado_em.is_(None),
                    )
                )
            ).scalar_one_or_none()
            if not sessao:
                raise SessaoDeServicosNaoEncontrado

            return SessaoDeServicos(
                id=sessao.id,
                cpf_do_cliente=sessao.cpf_do_cliente,
                nome_do_cliente=sessao.nome_do_cliente,
                data_inicio_da_realizacao=sessao.data_inicio_da_realizacao,
                data_final_da_realizacao=sessao.data_final_da_realizacao,
                valor_total=sessao.valor_total,
                valor_desconto=sessao.valor_desconto,
                valor_pago=sessao.valor_pago,
                valor_restante=sessao.valor_restante,
                forma_de_pagamento=sessao.forma_de_pagamento,
                observacoes=sessao.observacoes,
                registros=[
                    RegistroDeServico(
                        id=registro.id,
                        codigo_sessao_de_servicos=registro.codigo_sessao_de_servicos,
                        codigo_servico=registro.codigo_servico,
                        nome=registro.nome,
                        valor=registro.valor,
                        descricao=registro.descricao,
                        data_realizacao=registro.data_realizacao,
                    )
                    for registro in sessao.registros
                ],
            )

    async def _adicionar(self, sessao: SessaoDeServicos) -> None:
        dados = {
            "id": sessao.id,
            "id_cliente": sessao.id_cliente,
            "cpf_do_cliente": sessao.cpf_do_cliente,
            "nome_do_cliente": sessao.nome_do_cliente,
            "data_inicio_da_realizacao": sessao.data_inicio_da_realizacao,
            "data_final_da_realizacao": sessao.data_final_da_realizacao,
            "valor_total": sessao.valor_total,
            "valor_desconto": sessao.valor_desconto,
            "valor_pago": sessao.valor_pago,
            "valor_restante": sessao.valor_restante,
            "forma_de_pagamento": sessao.forma_de_pagamento,
            "observacoes": sessao.observacoes,
            "criado_por": sessao.criado_por,
            "criado_em": sessao.criado_em,
            "modificado_por": sessao.modificado_por,
            "ultima_modificacao_em": sessao.ultima_modificacao_em,
            "deletado_por": sessao.deletado_por,
            "deletado_em": sessao.deletado_em,
        }

        match sessao._tipo_de_operacao:
            case TipoDeOperacao.INSERCAO:
                operacao = insert(SessaoDeServicosDB).values(dados)
            case TipoDeOperacao.ATUALIZACAO:
                operacao = (
                    update(SessaoDeServicosDB)
                    .where(SessaoDeServicosDB.id == sessao.id)
                    .values(dados)
                )
            case _:
                raise ValueError(
                    "Tipo de operação não suportado para o repositório de domínio."
                )

        await self.session.execute(operacao)

    async def _remover(self, sessao: SessaoDeServicos) -> None:
        if sessao._usa_soft_delete:
            dados = {
                "modificado_por": sessao.modificado_por,
                "ultima_modificacao_em": sessao.ultima_modificacao_em,
                "deletado_por": sessao.deletado_por,
                "deletado_em": sessao.deletado_em,
            }

            operacao = (
                update(SessaoDeServicosDB)
                .where(SessaoDeServicosDB.id == sessao.id)
                .values(dados)
            )
        else:
            operacao = delete(SessaoDeServicosDB).where(
                SessaoDeServicosDB.id == sessao.id
            )

        await self.session.execute(operacao)
