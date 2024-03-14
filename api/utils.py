from http.client import HTTPException

from fastapi import Depends
from fastapi.security import HTTPBearer
from starlette import status

security = HTTPBearer(scheme_name='Authorization')


def get_token(authorization: str = Depends(security), secret_vault=Depends(conn_vault)):
    """Get token from vault and comparing with input token
    :param authorization: input bearer token
    :type authorization: HTTPBearer
    :param secret_vault: token from vault
    :type secret_vault: str
    :return: token from vault
    """
    token = authorization.credentials
    if token != secret_vault:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Bearer token missing or unknown',
        )
    return token
