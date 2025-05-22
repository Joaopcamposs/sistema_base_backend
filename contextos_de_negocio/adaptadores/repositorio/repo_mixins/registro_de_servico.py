# from abc import ABC
#
# from sqlalchemy.ext.asyncio import AsyncSession
#
#
# class RegistroDeServicoMixin(ABC):
#     session: AsyncSession
#
#     async def _gerar_agregados_dos_registros_para_cadastro(
#         self,
#         id_sessao_de_servicos: UUID,
#         id_servico: UUID,
#         valor: Decimal,
#         data_realizacao: datetime,
#     ) -> RegistroDeServico:
#         async with self.session as session:
#             sessao_de_servicos = (
#                 await session.execute(
#                     select(SessaoDeServicosDB).where(
#                         SessaoDeServicosDB.id == id_sessao_de_servicos,
#                         SessaoDeServicosDB.deletado_em.is_(None),
#                     )
#                 )
#             ).scalar_one_or_none()
#             if not sessao_de_servicos:
#                 raise SessaoDeServicosNaoEncontrado
#
#             servico = (
#                 await session.execute(
#                     select(ServicoDB).where(
#                         ServicoDB.id == id_servico, ServicoDB.deletado_em.is_(None)
#                     )
#                 )
#             ).scalar_one_or_none()
#             if not servico:
#                 raise ServicoNaoEncontrado
#
#             return RegistroDeServico.retornar_agregado_para_cadastro(
#                 id_sessao_de_servicos=id_sessao_de_servicos,
#                 id_servico=id_servico,
#                 codigo=servico.codigo,
#                 nome=servico.nome,
#                 valor=valor or servico.valor,
#                 descricao=servico.descricao,
#                 data_realizacao=data_realizacao,
#             )
