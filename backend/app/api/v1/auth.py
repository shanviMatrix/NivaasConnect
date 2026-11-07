from fastapi import APIRouter, Depends, HTTPException, Request, status
from psycopg.errors import ForeignKeyViolation, UniqueViolation
from psycopg.rows import dict_row

from app.api.dependencies import get_current_user, require_roles
from app.core.config import settings
from app.core.security import create_access_token, hash_password, verify_password
from app.schemas.auth import AccountCreate, LoginRequest


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login")
async def login(data: LoginRequest, request: Request):
    async with request.app.state.db_pool.connection() as connection:
        async with connection.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(
                """
                SELECT account_id, username, password_hash, role,
                       resident_id, guard_id, is_active
                FROM user_accounts
                WHERE username = %s
                """,
                (data.username.strip(),),
            )
            account = await cursor.fetchone()

    if (
        not account
        or not account["is_active"]
        or not verify_password(data.password, account["password_hash"])
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {
        "access_token": create_access_token(account),
        "token_type": "bearer",
        "expires_in": settings.access_token_expire_minutes * 60,
        "user": {
            "account_id": account["account_id"],
            "username": account["username"],
            "role": account["role"],
            "resident_id": account["resident_id"],
            "guard_id": account["guard_id"],
        },
    }


@router.get("/me")
async def get_my_profile(
    current_user: dict = Depends(get_current_user),
):
    return current_user


@router.post("/accounts", status_code=status.HTTP_201_CREATED)
async def create_account(
    data: AccountCreate,
    request: Request,
    admin: dict = Depends(require_roles("Admin")),
):
    pool = request.app.state.db_pool

    async with pool.connection() as connection:
        async with connection.cursor() as cursor:
            if data.role == "Resident":
                await cursor.execute(
                    """
                    SELECT resident_id
                    FROM residents
                    WHERE resident_id = %s
                    """,
                    (data.resident_id,),
                )
            else:
                await cursor.execute(
                    """
                    SELECT guard_id
                    FROM security_guards
                    WHERE guard_id = %s AND is_active = TRUE
                    """,
                    (data.guard_id,),
                )

            if await cursor.fetchone() is None:
                raise HTTPException(
                    status_code=404,
                    detail="The linked resident or active security guard was not found.",
                )

            try:
                await cursor.execute(
                    """
                    INSERT INTO user_accounts
                        (username, password_hash, role, resident_id, guard_id)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING account_id, username, role,
                              resident_id, guard_id, is_active, created_at
                    """,
                    (
                        data.username,
                        hash_password(data.password),
                        data.role,
                        data.resident_id,
                        data.guard_id,
                    ),
                )
                account = await cursor.fetchone()

            except UniqueViolation:
                raise HTTPException(
                    status_code=409,
                    detail="Username or linked user account already exists.",
                )
            except ForeignKeyViolation:
                raise HTTPException(
                    status_code=404,
                    detail="The linked resident or security guard no longer exists.",
                )

    return account
