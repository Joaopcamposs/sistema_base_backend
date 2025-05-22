from barramento_de_mensagens.dominio import DominioBase

from contextos_de_negocio.adaptadores.repositorio.repo_consulta.cliente import (
    ClienteRepoConsulta,
)
from contextos_de_negocio.adaptadores.repositorio.repo_consulta.empresa import (
    EmpresaRepoConsulta,
)
from contextos_de_negocio.adaptadores.repositorio.repo_consulta.servico import (
    ServicoRepoConsulta,
)
from contextos_de_negocio.adaptadores.repositorio.repo_consulta.usuario import (
    UsuarioRepoConsulta,
)
from contextos_de_negocio.adaptadores.repositorio.repo_dominio.cliente import (
    ClienteRepoDominio,
)
from contextos_de_negocio.adaptadores.repositorio.repo_dominio.empresa import (
    EmpresaRepoDominio,
)
from contextos_de_negocio.adaptadores.repositorio.repo_dominio.servico import (
    ServicoRepoDominio,
)
from contextos_de_negocio.adaptadores.repositorio.repo_dominio.usuario import (
    UsuarioRepoDominio,
)


class Dominio(DominioBase):
    usuario = (UsuarioRepoDominio, UsuarioRepoConsulta)
    empresa = (EmpresaRepoDominio, EmpresaRepoConsulta)
    cliente = (ClienteRepoDominio, ClienteRepoConsulta)
    servico = (ServicoRepoDominio, ServicoRepoConsulta)
    # historico_servico = (HistoricoServicoRepoDominio, HistoricoServicoRepoConsulta)
    # registro_servico = (RegistroServicoRepoDominio, RegistroServicoRepoConsulta)
