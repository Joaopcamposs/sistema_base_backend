from fastapi import APIRouter
from starlette.responses import JSONResponse

from contextos_de_negocio.barramento import bootstrap
from contextos_de_negocio.dominio.comandos.teste import ComandoTeste
from contextos_de_negocio.dominio.entidades.usuario import UsuarioEntidade

router_teste = APIRouter(prefix="/api/v1", tags=["Teste"])


@router_teste.post("/comando_teste")
async def comando_teste_api(
    mensagem: str,
):
    from uuid import uuid4

    usuario = UsuarioEntidade(
        id=uuid4(),
        empresa=uuid4(),
        nome="joao",
        email="joao",
        cpf="123",
        ativo=True,
        adm=True,
        _senha="134",
    )

    bus = bootstrap(usuario=usuario)

    comando = ComandoTeste(mensagem)
    retorno = await bus.handle(comando)

    return JSONResponse(status_code=201, content=str(retorno))
