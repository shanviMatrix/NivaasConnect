import jwt

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from psycopg.rows import dict_row

from app.core.config import settings


bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
):
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired authentication token.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if credentials is None:
        raise unauthorized

    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )
        account_id = int(payload.get("sub", ""))
        if account_id <= 0:
            raise unauthorized
    except (jwt.InvalidTokenError, ValueError, TypeError):
        raise unauthorized

    async with request.app.state.db_pool.connection() as connection:
        async with connection.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(
                """
                SELECT account_id, username, role,
                       resident_id, guard_id, is_active
                FROM user_accounts
                WHERE account_id = %s
                """,
                (account_id,),
            )
            account = await cursor.fetchone()

    if not account or not account["is_active"]:
        raise unauthorized

    return account


def require_roles(*allowed_roles: str):
    async def role_checker(
        current_user: dict = Depends(get_current_user),
    ):
        if current_user["role"] not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource.",
            )
        return current_user

    return role_checker


async def authorize_resource_access(
    request: Request,
    current_user: dict = Depends(get_current_user),
):
    role = current_user["role"]

    if role == "Admin":
        return current_user

    relative_path = request.url.path.removeprefix(
        settings.api_v1_prefix
    ).strip("/")
    parts = relative_path.split("/")
    resource = parts[0] if parts else ""

    # Shared information that residents and security may read.
    if (
        request.method == "GET"
        and resource in {"vendors", "facilities", "society-events"}
        and role in {"Resident", "Security"}
    ):
        return current_user

    # A resident may only access their own profile endpoint.
    if (
        request.method == "GET"
        and parts == ["residents", "me"]
        and role == "Resident"
    ):
        return current_user

    # A security guard may only access their own profile endpoint.
    if (
        request.method == "GET"
        and parts == ["security-guards", "me"]
        and role == "Security"
    ):
        return current_user

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You do not have permission to access this resource.",
    )
