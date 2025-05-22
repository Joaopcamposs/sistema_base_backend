from barramento_de_mensagens.dominio import DominioBase

from contextos_de_negocio.adaptadores.repositorio.repo_consulta.cliente import (
    ClienteRepoConsulta,
)
from contextos_de_negocio.adaptadores.repositorio.repo_consulta.empresa import (
    EmpresaRepoConsulta,
)
from contextos_de_negocio.adaptadores.repositorio.repo_consulta.registro_de_servico import (
    RegistroDeServicoRepoConsulta,
)
from contextos_de_negocio.adaptadores.repositorio.repo_consulta.servico import (
    ServicoRepoConsulta,
)
from contextos_de_negocio.adaptadores.repositorio.repo_consulta.sessao_de_servicos import (
    SessaoDeServicosRepoConsulta,
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
from contextos_de_negocio.adaptadores.repositorio.repo_dominio.registro_de_servico import (
    RegistroDeServicoRepoDominio,
)
from contextos_de_negocio.adaptadores.repositorio.repo_dominio.servico import (
    ServicoRepoDominio,
)
from contextos_de_negocio.adaptadores.repositorio.repo_dominio.sessao_de_servicos import (
    SessaoDeServicosRepoDominio,
)
from contextos_de_negocio.adaptadores.repositorio.repo_dominio.usuario import (
    UsuarioRepoDominio,
)


class Dominio(DominioBase):
    usuario = (UsuarioRepoDominio, UsuarioRepoConsulta)
    empresa = (EmpresaRepoDominio, EmpresaRepoConsulta)
    cliente = (ClienteRepoDominio, ClienteRepoConsulta)
    servico = (ServicoRepoDominio, ServicoRepoConsulta)
    registro_de_servico = (RegistroDeServicoRepoDominio, RegistroDeServicoRepoConsulta)
    sessao_de_servicos = (SessaoDeServicosRepoDominio, SessaoDeServicosRepoConsulta)
