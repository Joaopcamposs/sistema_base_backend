from abc import abstractmethod
from sqlalchemy import select, insert, update, delete

from contextos_de_negocio.adaptadores.orm.declarativo.cliente import ClienteDB
from contextos_de_negocio.dominio.agregados.cliente import Cliente
from contextos_de_negocio.dominio.entidades.cliente import Endereco
from contextos_de_negocio.dominio.excecoes import (
    ClienteNaoEncontrado,
    ClienteJaCadastrado,
)
from libs.ddd.adaptadores.repositorio.repositorio import RepositorioDominio
from libs.ddd.adaptadores.visualizadores.visualizadores import Filtros
from libs.utils.constantes import NAO_DELETADO
from libs.utils.tipos_basicos import Email, TipoDeOperacao, CPF


class ClienteRepoDominioAbstrato(RepositorioDominio):
    def __init__(self, *args, **kwargs):
        super(ClienteRepoDominioAbstrato, self).__init__(*args, **kwargs)
        self.seen: set[Cliente] = set()

    async def adicionar(self, cliente: Cliente) -> None:
        self.seen.add(cliente)
        await self._adicionar(cliente)

    @abstractmethod
    async def _adicionar(self, cliente: Cliente) -> None:
        raise NotImplementedError

    async def remover(self, cliente: Cliente) -> None:
        await self._remover(cliente)

    @abstractmethod
    async def _remover(self, cliente: Cliente) -> None:
        raise NotImplementedError

    @abstractmethod
    async def consultar_um_por_filtros(self, filtros: Filtros) -> Cliente:
        raise NotImplementedError()


class ClienteRepoDominio(ClienteRepoDominioAbstrato):
    async def gerar_agregado_para_cadastro(
        self,
        nome: str,
        cpf: str,
        telefone: str,
        telefone_2: str,
        email: str,
        endereco: Endereco,
    ) -> Cliente:
        async with self.session as session:
            cliente_com_mesmo_email = (
                await session.execute(
                    select(ClienteDB).where(
                        ClienteDB.email == Email(email), ClienteDB.deletado_em.is_(None)
                    )
                )
            ).scalar_one_or_none()
            if cliente_com_mesmo_email:
                raise ClienteJaCadastrado

        return Cliente.retornar_agregado_para_cadastro(
            nome=nome,
            cpf=CPF(cpf),
            telefone=telefone,
            telefone_2=telefone_2,
            email=Email(email),
            endereco=endereco,
        )

    async def consultar_um_por_filtros(self, filtros: Filtros) -> Cliente:
        async with self.session as session:
            cliente = (
                await session.execute(
                    select(ClienteDB).filter_by(**filtros, **NAO_DELETADO)
                )
            ).scalar_one_or_none()
            if not cliente:
                raise ClienteNaoEncontrado

            agregado = Cliente(
                id=cliente.id,
                nome=cliente.nome,
                cpf=CPF(cliente.cpf),
                telefone=cliente.telefone,
                telefone_2=cliente.telefone_2,
                email=Email(cliente.email),
                endereco=Endereco(
                    cep=cliente.cep,
                    rua=cliente.rua,
                    numero=cliente.numero,
                    complemento=cliente.complemento,
                    bairro=cliente.bairro,
                    cidade=cliente.cidade,
                    estado=cliente.estado,
                    pais=cliente.pais,
                ),
                criado_por=cliente.criado_por,
                criado_em=cliente.criado_em,
                ultima_modificacao_em=cliente.ultima_modificacao_em,
                modificado_por=cliente.modificado_por,
                deletado_em=cliente.deletado_em,
                deletado_por=cliente.deletado_por,
            )

        return agregado

    async def _adicionar(self, cliente: Cliente) -> None:
        dados = {
            "id": cliente.id,
            "nome": cliente.nome,
            "cpf": cliente.cpf,
            "telefone": cliente.telefone,
            "telefone_2": cliente.telefone_2,
            "email": cliente.email,
            "endereco": cliente.endereco,
            "criado_por": cliente.criado_por,
            "criado_em": cliente.criado_em,
            "modificado_por": cliente.modificado_por,
            "ultima_modificacao_em": cliente.ultima_modificacao_em,
            "deletado_por": cliente.deletado_por,
            "deletado_em": cliente.deletado_em,
        }

        match cliente._tipo_de_operacao:
            case TipoDeOperacao.INSERCAO:
                operacao = insert(ClienteDB).values(dados)
            case TipoDeOperacao.ATUALIZACAO:
                operacao = (
                    update(ClienteDB).where(ClienteDB.id == cliente.id).values(dados)
                )
            case _:
                raise ValueError(
                    "Tipo de operação não suportado para o repositório de domínio."
                )

        await self.session.execute(operacao)

    async def _remover(self, cliente: Cliente) -> None:
        if cliente._usa_soft_delete:
            dados = {
                "modificado_por": cliente.modificado_por,
                "ultima_modificacao_em": cliente.ultima_modificacao_em,
                "deletado_por": cliente.deletado_por,
                "deletado_em": cliente.deletado_em,
            }

            operacao = update(ClienteDB).where(ClienteDB.id == cliente.id).values(dados)
        else:
            operacao = delete(ClienteDB).where(ClienteDB.id == cliente.id)

        await self.session.execute(operacao)
