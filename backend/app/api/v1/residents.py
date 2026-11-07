from fastapi import APIRouter, HTTPException, Query, Request, Response, status
from psycopg.errors import ForeignKeyViolation, UniqueViolation

from app.schemas.resident import (
    ResidentCreate,
    ResidentDetailResponse,
    ResidentResponse,
    ResidentUpdate,
)
from app.services import resident_service

router = APIRouter(prefix="/residents", tags=["Residents"])


@router.get("", response_model=list[ResidentDetailResponse])
async def list_residents(
    request: Request,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    return await resident_service.get_residents(
        request.app.state.db_pool, limit, offset
    )


@router.post(
    "",
    response_model=ResidentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_resident(data: ResidentCreate, request: Request):
    try:
        return await resident_service.create_resident(
            request.app.state.db_pool,
            data.model_dump(),
        )
    except UniqueViolation:
        raise HTTPException(
            status_code=409,
            detail="A resident with this email already exists.",
        )
    except ForeignKeyViolation:
        raise HTTPException(
            status_code=404,
            detail="The specified apartment does not exist.",
        )


@router.get("/{resident_id}", response_model=ResidentDetailResponse)
async def read_resident(resident_id: int, request: Request):
    resident = await resident_service.get_resident(
        request.app.state.db_pool, resident_id
    )
    if resident is None:
        raise HTTPException(status_code=404, detail="Resident not found.")
    return resident


@router.put("/{resident_id}", response_model=ResidentResponse)
async def edit_resident(
    resident_id: int,
    data: ResidentUpdate,
    request: Request,
):
    try:
        resident = await resident_service.update_resident(
            request.app.state.db_pool,
            resident_id,
            data.model_dump(),
        )
    except UniqueViolation:
        raise HTTPException(
            status_code=409,
            detail="A resident with this email already exists.",
        )
    except ForeignKeyViolation:
        raise HTTPException(
            status_code=404,
            detail="The specified apartment does not exist.",
        )

    if resident is None:
        raise HTTPException(status_code=404, detail="Resident not found.")
    return resident


@router.delete("/{resident_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_resident(resident_id: int, request: Request):
    deleted = await resident_service.delete_resident(
        request.app.state.db_pool, resident_id
    )

    if deleted is None:
        raise HTTPException(status_code=404, detail="Resident not found.")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
