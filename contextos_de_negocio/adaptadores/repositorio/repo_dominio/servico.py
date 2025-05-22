from datetime import datetime

from contextos_de_negocio.adaptadores.orm.declarativo import (
    ClienteDB,
    ServicoDB,
    HistoricoServicosDB,
    RegistroServicoDB,
)
from infra.banco_de_dados import get_session

async with get_session(schema="", somente_leitura=False) as sessao:
    # cria cliente
    cliente = ClienteDB(nome="Maria", cpf="12345678900")
    sessao.add(cliente)
    sessao.commit()

    # busca cliente e modelo
    cliente = sessao.query(ClienteDB).filter_by(nome="Maria").one()
    modelo = sessao.query(ServicoDB).filter_by(nome="Limpeza Dental").one()

    # garante que o cliente tenha ficha
    if cliente.ficha_clinica is None:
        ficha = HistoricoServicosDB(cliente=cliente)
        sessao.add(ficha)
        sessao.commit()
    else:
        ficha = cliente.ficha_clinica

    # cria registro com snapshot
    registro = RegistroServicoDB(
        ficha_clinica_id=ficha.id,
        modelo_id=modelo.id,
        nome_procedimento=modelo.nome,
        valor_procedimento=modelo.valor_base,
        data_realizacao=datetime.utcnow(),
    )
    sessao.add(registro)
    sessao.commit()
