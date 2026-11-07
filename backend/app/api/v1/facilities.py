from fastapi import APIRouter, HTTPException, Query, Request, Response, status
from psycopg.errors import ForeignKeyViolation, UniqueViolation

from app.schemas.facility import FacilityCreate, FacilityResponse, FacilityUpdate
from app.services import facility_service

router = APIRouter(prefix="/facilities", tags=["Facilities"])


@router.get("", response_model=list[FacilityResponse])
async def list_facilities(
    request: Request,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    return await facility_service.get_facilities(request.app.state.db_pool, limit, offset)


@router.post("", response_model=FacilityResponse, status_code=201)
async def create_facility(data: FacilityCreate, request: Request):
    try:
        return await facility_service.create_facility(
            request.app.state.db_pool, data.model_dump()
        )
    except UniqueViolation:
        raise HTTPException(status_code=409, detail="Facility name already exists.")


@router.get("/{facility_id}", response_model=FacilityResponse)
async def read_facility(facility_id: int, request: Request):
    facility = await facility_service.get_facility(request.app.state.db_pool, facility_id)
    if facility is None:
        raise HTTPException(status_code=404, detail="Facility not found.")
    return facility


@router.put("/{facility_id}", response_model=FacilityResponse)
async def edit_facility(facility_id: int, data: FacilityUpdate, request: Request):
    try:
        facility = await facility_service.update_facility(
            request.app.state.db_pool, facility_id, data.model_dump()
        )
    except UniqueViolation:
        raise HTTPException(status_code=409, detail="Facility name already exists.")

    if facility is None:
        raise HTTPException(status_code=404, detail="Facility not found.")
    return facility


@router.delete("/{facility_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_facility(facility_id: int, request: Request):
    try:
        deleted = await facility_service.delete_facility(
            request.app.state.db_pool, facility_id
        )
    except ForeignKeyViolation:
        raise HTTPException(
            status_code=409,
            detail="This facility has bookings and cannot be deleted.",
        )

    if deleted is None:
        raise HTTPException(status_code=404, detail="Facility not found.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
