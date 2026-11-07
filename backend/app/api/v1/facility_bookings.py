from fastapi import APIRouter, HTTPException, Query, Request
from psycopg.errors import ForeignKeyViolation

from app.schemas.facility_booking import (
    FacilityBookingCreate,
    FacilityBookingResponse,
    FacilityBookingStatusUpdate,
)
from app.services import facility_booking_service

router = APIRouter(prefix="/facility-bookings", tags=["Facility Bookings"])


@router.get("", response_model=list[FacilityBookingResponse])
async def list_bookings(
    request: Request,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    return await facility_booking_service.get_bookings(
        request.app.state.db_pool, limit, offset
    )


@router.post("", response_model=FacilityBookingResponse, status_code=201)
async def create_booking(data: FacilityBookingCreate, request: Request):
    try:
        result = await facility_booking_service.create_booking(
            request.app.state.db_pool, data.model_dump()
        )
    except ForeignKeyViolation:
        raise HTTPException(
            status_code=404, detail="The specified resident does not exist."
        )

    if isinstance(result, dict) and "error" in result:
        errors = {
            "facility_not_found": (404, "Facility not found."),
            "facility_inactive": (409, "This facility is inactive."),
            "booking_conflict": (409, "This facility is already booked during that time."),
        }
        code, message = errors[result["error"]]
        raise HTTPException(status_code=code, detail=message)

    return result


@router.get("/{booking_id}", response_model=FacilityBookingResponse)
async def read_booking(booking_id: int, request: Request):
    booking = await facility_booking_service.get_booking(
        request.app.state.db_pool, booking_id
    )
    if booking is None:
        raise HTTPException(status_code=404, detail="Booking not found.")
    return booking


@router.put("/{booking_id}/status", response_model=FacilityBookingResponse)
async def edit_booking_status(
    booking_id: int,
    data: FacilityBookingStatusUpdate,
    request: Request,
):
    booking = await facility_booking_service.update_booking_status(
        request.app.state.db_pool, booking_id, data.booking_status
    )
    if booking is None:
        raise HTTPException(status_code=404, detail="Booking not found.")
    return booking
