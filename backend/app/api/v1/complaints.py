from fastapi import APIRouter, HTTPException, Query, Request, Response, status
from psycopg.errors import ForeignKeyViolation

from app.schemas.complaint import (
    ComplaintCreate,
    ComplaintResponse,
    ComplaintUpdate,
)
from app.services import complaint_service

router = APIRouter(prefix="/complaints", tags=["Complaints"])


@router.get("", response_model=list[ComplaintResponse])
async def list_complaints(
    request: Request,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    return await complaint_service.get_complaints(
        request.app.state.db_pool, limit, offset
    )


@router.post(
    "", response_model=ComplaintResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_complaint(data: ComplaintCreate, request: Request):
    try:
        return await complaint_service.create_complaint(
            request.app.state.db_pool, data.model_dump()
        )
    except ForeignKeyViolation:
        raise HTTPException(
            status_code=404,
            detail="The specified resident or vendor does not exist.",
        )


@router.get("/{complaint_id}", response_model=ComplaintResponse)
async def read_complaint(complaint_id: int, request: Request):
    complaint = await complaint_service.get_complaint(
        request.app.state.db_pool, complaint_id
    )
    if complaint is None:
        raise HTTPException(status_code=404, detail="Complaint not found.")
    return complaint


@router.put("/{complaint_id}", response_model=ComplaintResponse)
async def edit_complaint(
    complaint_id: int, data: ComplaintUpdate, request: Request
):
    try:
        complaint = await complaint_service.update_complaint(
            request.app.state.db_pool, complaint_id, data.model_dump()
        )
    except ForeignKeyViolation:
        raise HTTPException(
            status_code=404,
            detail="The specified resident or vendor does not exist.",
        )

    if complaint is None:
        raise HTTPException(status_code=404, detail="Complaint not found.")
    return complaint


@router.delete("/{complaint_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_complaint(complaint_id: int, request: Request):
    deleted = await complaint_service.delete_complaint(
        request.app.state.db_pool, complaint_id
    )
    if deleted is None:
        raise HTTPException(status_code=404, detail="Complaint not found.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
