from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response, status
from psycopg.errors import UniqueViolation

from app.schemas.vendor import VendorCreate, VendorResponse, VendorUpdate
from app.services import vendor_service

from app.api.dependencies import authorize_resource_access

router = APIRouter(dependencies=[Depends(authorize_resource_access)], prefix="/vendors", tags=["Vendors"])


@router.get("", response_model=list[VendorResponse])
async def list_vendors(
    request: Request,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    return await vendor_service.get_vendors(
        request.app.state.db_pool, limit, offset
    )


@router.post("", response_model=VendorResponse, status_code=status.HTTP_201_CREATED)
async def create_vendor(data: VendorCreate, request: Request):
    try:
        return await vendor_service.create_vendor(
            request.app.state.db_pool, data.model_dump()
        )
    except UniqueViolation:
        raise HTTPException(
            status_code=409,
            detail="A vendor with this email already exists.",
        )


@router.get("/{vendor_id}", response_model=VendorResponse)
async def read_vendor(vendor_id: int, request: Request):
    vendor = await vendor_service.get_vendor(
        request.app.state.db_pool, vendor_id
    )
    if vendor is None:
        raise HTTPException(status_code=404, detail="Vendor not found.")
    return vendor


@router.put("/{vendor_id}", response_model=VendorResponse)
async def edit_vendor(vendor_id: int, data: VendorUpdate, request: Request):
    try:
        vendor = await vendor_service.update_vendor(
            request.app.state.db_pool, vendor_id, data.model_dump()
        )
    except UniqueViolation:
        raise HTTPException(
            status_code=409,
            detail="A vendor with this email already exists.",
        )

    if vendor is None:
        raise HTTPException(status_code=404, detail="Vendor not found.")
    return vendor


@router.delete("/{vendor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_vendor(vendor_id: int, request: Request):
    deleted = await vendor_service.delete_vendor(
        request.app.state.db_pool, vendor_id
    )
    if deleted is None:
        raise HTTPException(status_code=404, detail="Vendor not found.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
