from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response, status
from psycopg.errors import ForeignKeyViolation, UniqueViolation

from app.schemas.apartment import ApartmentCreate, ApartmentResponse, ApartmentUpdate
from app.services import apartment_service

from app.api.dependencies import require_roles

router = APIRouter(dependencies=[Depends(require_roles("Admin"))], prefix="/apartments", tags=["Apartments"])


@router.get("", response_model=list[ApartmentResponse])
async def list_apartments(
    request: Request,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    return await apartment_service.get_apartments(
        request.app.state.db_pool, limit, offset
    )


@router.post(
    "",
    response_model=ApartmentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_apartment(data: ApartmentCreate, request: Request):
    try:
        return await apartment_service.create_apartment(
            request.app.state.db_pool,
            data.model_dump(),
        )
    except UniqueViolation:
        raise HTTPException(
            status_code=409,
            detail="An apartment with this building and flat number already exists.",
        )


@router.get("/{apartment_id}", response_model=ApartmentResponse)
async def read_apartment(apartment_id: int, request: Request):
    apartment = await apartment_service.get_apartment(
        request.app.state.db_pool, apartment_id
    )
    if apartment is None:
        raise HTTPException(status_code=404, detail="Apartment not found.")
    return apartment


@router.put("/{apartment_id}", response_model=ApartmentResponse)
async def edit_apartment(
    apartment_id: int,
    data: ApartmentUpdate,
    request: Request,
):
    try:
        apartment = await apartment_service.update_apartment(
            request.app.state.db_pool,
            apartment_id,
            data.model_dump(),
        )
    except UniqueViolation:
        raise HTTPException(
            status_code=409,
            detail="An apartment with this building and flat number already exists.",
        )

    if apartment is None:
        raise HTTPException(status_code=404, detail="Apartment not found.")
    return apartment


@router.delete("/{apartment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_apartment(apartment_id: int, request: Request):
    try:
        deleted = await apartment_service.delete_apartment(
            request.app.state.db_pool, apartment_id
        )
    except ForeignKeyViolation:
        raise HTTPException(
            status_code=409,
            detail="Cannot delete this apartment because residents are assigned to it.",
        )

    if deleted is None:
        raise HTTPException(status_code=404, detail="Apartment not found.")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
