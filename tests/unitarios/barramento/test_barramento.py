"""
Testes unitários para o barramento de mensagens.
"""

import pytest
from uuid import uuid4
from dataclasses import dataclass
from unittest.mock import MagicMock

from libs.barramento_de_mensagens.base.barramento import (
    BarramentoDeMensagens,
    Comando,
    Evento,
)
from libs.barramento_de_mensagens.base.executor_assincrono import (
    ExecutorAssincronoNulo,
)


@dataclass
class ComandoTeste(Comando):
    """Comando de teste."""

    valor: str


@dataclass
class EventoTeste(Evento):
    """Evento de teste."""

    valor: str


class MockUnidadeDeTrabalho:
    """Mock da unidade de trabalho para testes."""

    def __init__(self):
        self.usuario = MagicMock()
        self.usuario.empresa = uuid4()
        self._eventos = []

    def collect_new_events(self):
        eventos = self._eventos.copy()
        self._eventos.clear()
        return eventos

    def adicionar_evento(self, evento):
        self._eventos.append(evento)


class TestBarramentoDeMensagens:
    """Testes para o BarramentoDeMensagens."""

    @pytest.fixture
    def mock_uow(self):
        """Fixture para mock da unidade de trabalho."""
        return MockUnidadeDeTrabalho()

    @pytest.fixture
    def executor_nulo(self):
        """Fixture para executor assíncrono nulo."""
        return ExecutorAssincronoNulo()

    @pytest.mark.asyncio
    async def test_deve_processar_comando(self, mock_uow):
        """Deve processar um comando corretamente."""
        resultado_esperado = "resultado_teste"

        async def handler_teste(comando: ComandoTeste):
            return resultado_esperado

        barramento = BarramentoDeMensagens(
            uow=mock_uow,
            event_handlers={},
            command_handlers={ComandoTeste: handler_teste},
        )

        comando = ComandoTeste(valor="teste")
        resultado = await barramento.handle(comando)

        assert resultado == resultado_esperado

    @pytest.mark.asyncio
    async def test_deve_processar_evento(self, mock_uow):
        """Deve processar um evento corretamente."""
        eventos_processados = []

        async def handler_evento(evento: EventoTeste):
            eventos_processados.append(evento)

        barramento = BarramentoDeMensagens(
            uow=mock_uow,
            event_handlers={EventoTeste: [handler_evento]},
            command_handlers={},
        )

        evento = EventoTeste(valor="teste_evento")
        await barramento.handle(evento)

        assert len(eventos_processados) == 1
        assert eventos_processados[0].valor == "teste_evento"

    @pytest.mark.asyncio
    async def test_deve_processar_multiplos_handlers_evento(self, mock_uow):
        """Deve processar múltiplos handlers para o mesmo evento."""
        resultados = []

        async def handler_1(evento: EventoTeste):
            resultados.append("handler_1")

        async def handler_2(evento: EventoTeste):
            resultados.append("handler_2")

        barramento = BarramentoDeMensagens(
            uow=mock_uow,
            event_handlers={EventoTeste: [handler_1, handler_2]},
            command_handlers={},
        )

        evento = EventoTeste(valor="teste")
        await barramento.handle(evento)

        assert len(resultados) == 2
        assert "handler_1" in resultados
        assert "handler_2" in resultados

    @pytest.mark.asyncio
    async def test_deve_coletar_eventos_gerados_por_comando(self, mock_uow):
        """Deve coletar e processar eventos gerados por comando."""
        eventos_processados = []

        async def handler_comando(comando: ComandoTeste):
            mock_uow.adicionar_evento(EventoTeste(valor="evento_gerado"))
            return "ok"

        async def handler_evento(evento: EventoTeste):
            eventos_processados.append(evento)

        barramento = BarramentoDeMensagens(
            uow=mock_uow,
            event_handlers={EventoTeste: [handler_evento]},
            command_handlers={ComandoTeste: handler_comando},
        )

        comando = ComandoTeste(valor="gerar_evento")
        await barramento.handle(comando)

        assert len(eventos_processados) == 1
        assert eventos_processados[0].valor == "evento_gerado"

    @pytest.mark.asyncio
    async def test_deve_lancar_excecao_em_comando_sem_handler(self, mock_uow):
        """Deve lançar exceção quando não há handler para o comando."""
        barramento = BarramentoDeMensagens(
            uow=mock_uow,
            event_handlers={},
            command_handlers={},
        )

        comando = ComandoTeste(valor="sem_handler")

        with pytest.raises(KeyError):
            await barramento.handle(comando)

    @pytest.mark.asyncio
    async def test_deve_ignorar_evento_sem_handler(self, mock_uow):
        """Deve ignorar evento sem handler configurado."""
        barramento = BarramentoDeMensagens(
            uow=mock_uow,
            event_handlers={},
            command_handlers={},
        )

        evento = EventoTeste(valor="sem_handler")
        # Não deve lançar exceção
        await barramento.handle(evento)

    @pytest.mark.asyncio
    async def test_deve_usar_executor_assincrono_para_evento_assincrono(
        self, mock_uow, executor_nulo
    ):
        """Deve usar executor assíncrono para eventos marcados como assíncronos."""
        barramento = BarramentoDeMensagens(
            uow=mock_uow,
            event_handlers={EventoTeste: []},
            command_handlers={},
            permitir_execucoes_assincronas=True,
            executor_assincrono=executor_nulo,
        )

        evento = EventoTeste(
            valor="assincrono",
            executar_de_forma_assincrona=True,
        )
        await barramento.handle(evento)

        assert len(executor_nulo.eventos_executados) == 1
        assert executor_nulo.eventos_executados[0][0].valor == "assincrono"

    @pytest.mark.asyncio
    async def test_deve_executar_sincronamente_sem_executor_configurado(self, mock_uow):
        """Deve executar sincronamente quando não há executor configurado."""
        eventos_processados = []

        async def handler_evento(evento: EventoTeste):
            eventos_processados.append(evento)

        barramento = BarramentoDeMensagens(
            uow=mock_uow,
            event_handlers={EventoTeste: [handler_evento]},
            command_handlers={},
            permitir_execucoes_assincronas=True,
            executor_assincrono=None,  # Sem executor
        )

        evento = EventoTeste(
            valor="sem_executor",
            executar_de_forma_assincrona=True,
        )
        await barramento.handle(evento)

        # Deve ter processado sincronamente
        assert len(eventos_processados) == 1

    @pytest.mark.asyncio
    async def test_deve_subir_erro_de_comando(self, mock_uow):
        """Deve propagar exceção de handler de comando."""

        async def handler_com_erro(comando: ComandoTeste):
            raise ValueError("Erro no comando")

        barramento = BarramentoDeMensagens(
            uow=mock_uow,
            event_handlers={},
            command_handlers={ComandoTeste: handler_com_erro},
        )

        comando = ComandoTeste(valor="erro")

        with pytest.raises(ValueError, match="Erro no comando"):
            await barramento.handle(comando)

    @pytest.mark.asyncio
    async def test_deve_subir_erro_de_evento_quando_configurado(self, mock_uow):
        """Deve propagar exceção de handler de evento quando configurado."""

        async def handler_com_erro(evento: EventoTeste):
            raise ValueError("Erro no evento")

        barramento = BarramentoDeMensagens(
            uow=mock_uow,
            event_handlers={EventoTeste: [handler_com_erro]},
            command_handlers={},
            subir_erros_de_eventos=True,
        )

        evento = EventoTeste(valor="erro")

        with pytest.raises(ValueError, match="Erro no evento"):
            await barramento.handle(evento)


class TestExecutorAssincronoNulo:
    """Testes para o ExecutorAssincronoNulo."""

    def test_deve_registrar_evento_executado(self):
        """Deve registrar evento executado."""
        executor = ExecutorAssincronoNulo()
        evento = EventoTeste(valor="teste")
        usuario = MagicMock()

        executor.executar(evento=evento, usuario=usuario)

        assert len(executor.eventos_executados) == 1
        assert executor.eventos_executados[0] == (evento, usuario)

    def test_deve_limpar_eventos_executados(self):
        """Deve limpar lista de eventos executados."""
        executor = ExecutorAssincronoNulo()
        evento = EventoTeste(valor="teste")

        executor.executar(evento=evento)
        executor.limpar()

        assert len(executor.eventos_executados) == 0


class TestExecutorAssincronoAbstrato:
    """Testes para o ExecutorAssincronoAbstrato."""

    def test_deve_configurar_tarefa_com_countdown(self):
        """Deve configurar tarefa com countdown."""
        executor = ExecutorAssincronoNulo()
        evento = EventoTeste(
            valor="teste",
            tempo_de_atraso_para_execucao_assincrona=30,
        )

        config = executor.configurar_tarefa(evento)

        assert config["countdown"] == 30

    def test_deve_configurar_tarefa_com_fila(self):
        """Deve configurar tarefa com fila específica."""
        executor = ExecutorAssincronoNulo()
        evento = EventoTeste(
            valor="teste",
            fila_de_execucao_assincrona="fila_alta_prioridade",
        )

        config = executor.configurar_tarefa(evento)

        assert config["queue"] == "fila_alta_prioridade"

    def test_deve_configurar_tarefa_com_prioridade(self):
        """Deve configurar tarefa com prioridade."""
        executor = ExecutorAssincronoNulo()
        evento = EventoTeste(
            valor="teste",
            fila_de_execucao_assincrona="fila_teste",
            prioridade_de_execucao_assincrona=10,
        )

        config = executor.configurar_tarefa(evento)

        assert config["queue"] == "fila_teste"
        assert config["priority"] == 10

    def test_nao_deve_configurar_prioridade_sem_fila(self):
        """Não deve configurar prioridade sem fila definida."""
        executor = ExecutorAssincronoNulo()
        evento = EventoTeste(
            valor="teste",
            prioridade_de_execucao_assincrona=10,
        )

        config = executor.configurar_tarefa(evento)

        assert "priority" not in config
