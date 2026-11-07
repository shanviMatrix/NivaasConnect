from fastapi import APIRouter, HTTPException, Query, Request, Response, status
from psycopg.errors import ForeignKeyViolation, UniqueViolation

from app.schemas.maintenance_bill import (
    MaintenanceBillCreate,
    MaintenanceBillResponse,
    MaintenanceBillUpdate,
)
from app.services import maintenance_bill_service

router = APIRouter(prefix="/maintenance-bills", tags=["Maintenance Bills"])


@router.get("", response_model=list[MaintenanceBillResponse])
async def list_bills(
    request: Request,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    return await maintenance_bill_service.get_bills(
        request.app.state.db_pool, limit, offset
    )


@router.post(
    "", response_model=MaintenanceBillResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_bill(data: MaintenanceBillCreate, request: Request):
    try:
        return await maintenance_bill_service.create_bill(
            request.app.state.db_pool, data.model_dump()
        )
    except UniqueViolation:
        raise HTTPException(
            status_code=409,
            detail="A bill already exists for this apartment and billing month.",
        )
    except ForeignKeyViolation:
        raise HTTPException(status_code=404, detail="Apartment not found.")


@router.get("/{bill_id}", response_model=MaintenanceBillResponse)
async def read_bill(bill_id: int, request: Request):
    bill = await maintenance_bill_service.get_bill(
        request.app.state.db_pool, bill_id
    )
    if bill is None:
        raise HTTPException(status_code=404, detail="Maintenance bill not found.")
    return bill


@router.put("/{bill_id}", response_model=MaintenanceBillResponse)
async def edit_bill(
    bill_id: int, data: MaintenanceBillUpdate, request: Request
):
    try:
        bill = await maintenance_bill_service.update_bill(
            request.app.state.db_pool, bill_id, data.model_dump()
        )
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    except UniqueViolation:
        raise HTTPException(
            status_code=409,
            detail="A bill already exists for this apartment and billing month.",
        )
    except ForeignKeyViolation:
        raise HTTPException(status_code=404, detail="Apartment not found.")

    if bill is None:
        raise HTTPException(status_code=404, detail="Maintenance bill not found.")
    return bill


@router.delete("/{bill_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_bill(bill_id: int, request: Request):
    try:
        deleted = await maintenance_bill_service.delete_bill(
            request.app.state.db_pool, bill_id
        )
    except ForeignKeyViolation:
        raise HTTPException(
            status_code=409,
            detail="Cannot delete a bill that has payment records.",
        )

    if deleted is None:
        raise HTTPException(status_code=404, detail="Maintenance bill not found.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
