from fastapi import APIRouter, HTTPException, Query, Request, Response, status
from psycopg.errors import UniqueViolation

from app.schemas.security_guard import (
    SecurityGuardCreate,
    SecurityGuardResponse,
    SecurityGuardUpdate,
)
from app.services import security_guard_service

router = APIRouter(prefix="/security-guards", tags=["Security Guards"])


@router.get("", response_model=list[SecurityGuardResponse])
async def list_security_guards(
    request: Request,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    return await security_guard_service.get_security_guards(
        request.app.state.db_pool, limit, offset
    )


@router.post(
    "",
    response_model=SecurityGuardResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_security_guard(data: SecurityGuardCreate, request: Request):
    try:
        return await security_guard_service.create_security_guard(
            request.app.state.db_pool, data.model_dump()
        )
    except UniqueViolation:
        raise HTTPException(
            status_code=409,
            detail="A security guard with this phone number already exists.",
        )


@router.get("/{guard_id}", response_model=SecurityGuardResponse)
async def read_security_guard(guard_id: int, request: Request):
    guard = await security_guard_service.get_security_guard(
        request.app.state.db_pool, guard_id
    )
    if guard is None:
        raise HTTPException(status_code=404, detail="Security guard not found.")
    return guard


@router.put("/{guard_id}", response_model=SecurityGuardResponse)
async def edit_security_guard(
    guard_id: int, data: SecurityGuardUpdate, request: Request
):
    try:
        guard = await security_guard_service.update_security_guard(
            request.app.state.db_pool, guard_id, data.model_dump()
        )
    except UniqueViolation:
        raise HTTPException(
            status_code=409,
            detail="A security guard with this phone number already exists.",
        )

    if guard is None:
        raise HTTPException(status_code=404, detail="Security guard not found.")
    return guard


@router.delete("/{guard_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_security_guard(guard_id: int, request: Request):
    deleted = await security_guard_service.delete_security_guard(
        request.app.state.db_pool, guard_id
    )
    if deleted is None:
        raise HTTPException(status_code=404, detail="Security guard not found.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
