from sqlalchemy import select

from contextos_de_negocio.adaptadores.orm.declarativo.cliente import ClienteDB
from contextos_de_negocio.dominio.entidades.cliente import ClienteEntidade, Endereco
from libs.ddd.adaptadores.repositorio.repositorio import RepositorioConsulta
from libs.ddd.adaptadores.visualizadores.visualizadores import Filtros
from libs.utils.constantes import NAO_DELETADO
from libs.utils.tipos_basicos import Email, CPF


class ClienteRepoConsulta(RepositorioConsulta):
    async def consultar_um_por_email(self, email: str) -> ClienteEntidade | None:
        async with self.session as session:
            cliente = (
                await session.execute(
                    select(ClienteDB).where(
                        ClienteDB.email == email, ClienteDB.deletado_em.is_(None)
                    )
                )
            ).scalar_one_or_none()
            if not cliente:
                return None

            cliente_entidade = ClienteEntidade(
                id=cliente.id,
                nome=cliente.nome,
                email=Email(cliente.email),
                cpf=CPF(cliente.cpf),
                telefone=cliente.telefone,
                telefone_2=cliente.telefone_2,
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
            )

        return cliente_entidade

    async def consultar_um_por_filtros(self, filtros: Filtros) -> ClienteEntidade | None:
        async with self.session as session:
            cliente = (
                await session.execute(
                    select(ClienteDB).filter_by(**filtros, **NAO_DELETADO)
                )
            ).scalar_one_or_none()
            if not cliente:
                return None

            cliente_entidade = ClienteEntidade(
                id=cliente.id,
                nome=cliente.nome,
                email=Email(cliente.email),
                cpf=CPF(cliente.cpf),
                telefone=cliente.telefone,
                telefone_2=cliente.telefone_2,
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
            )

        return cliente_entidade

    async def consultar_por_filtros(self, filtros: Filtros) -> list[ClienteEntidade]:
        async with self.session as session:
            clientes = (
                (
                    await session.execute(
                        select(ClienteDB).filter_by(**filtros, **NAO_DELETADO)
                    )
                )
                .scalars()
                .all()
            )

            clientes_entidade = [
                ClienteEntidade(
                    id=cliente.id,
                    nome=cliente.nome,
                    email=Email(cliente.email),
                    cpf=CPF(cliente.cpf),
                    telefone=cliente.telefone,
                    telefone_2=cliente.telefone_2,
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
                )
                for cliente in clientes
            ]

        return clientes_entidade
