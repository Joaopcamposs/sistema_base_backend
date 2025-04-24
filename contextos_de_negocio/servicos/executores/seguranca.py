from contextvars import ContextVar
from datetime import timedelta, datetime
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, Security
from fastapi.security import SecurityScopes
from passlib.exc import InvalidTokenError
from pydantic import ValidationError
from starlette import status

from contextos_de_negocio.dominio.entidades.usuario import UsuarioEntidade
from contextos_de_negocio.pontos_de_entrada.schemas.seguranca import TokenData
from infra.banco_de_dados import DEFAULT_SQL_SESSION_FACTORY
from libs.utils.constantes import SECRET_KEY, ALGORITHM, oauth2_scheme

current_user: ContextVar[UsuarioEntidade] = ContextVar("current_user")


async def authenticate_user(username: str, password: str) -> bool | UsuarioEntidade:
    from contextos_de_negocio import UsuarioRepoConsulta

    async with DEFAULT_SQL_SESSION_FACTORY(somente_leitura=True) as session:
        repo = UsuarioRepoConsulta(session=session)
        usuario = await repo.consultar_um_por_email(email=username)

    if not usuario:
        return False
    if not usuario.verificar_senha(password):
        return False
    return usuario


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)]
):
    from contextos_de_negocio import UsuarioRepoConsulta

    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (InvalidTokenError, ValidationError):
        raise credentials_exception

    async with DEFAULT_SQL_SESSION_FACTORY(somente_leitura=True) as session:
        repo = UsuarioRepoConsulta(session=session)
        user = await repo.consultar_um_por_email(email=token_data.username)

    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    current_user.set(user)

    return user


async def get_current_active_user(
    current_user_ctx: Annotated[
        UsuarioEntidade, Security(get_current_user, scopes=["me"])
    ],
):
    if current_user_ctx.ativo:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user_ctx
