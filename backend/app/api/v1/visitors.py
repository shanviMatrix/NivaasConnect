from fastapi import APIRouter, HTTPException, Query, Request
from psycopg.errors import ForeignKeyViolation

from app.schemas.visitor import (
    VisitorApprovalUpdate,
    VisitorCreate,
    VisitorResponse,
)
from app.services import visitor_service

router = APIRouter(prefix="/visitors", tags=["Visitors"])


@router.get("", response_model=list[VisitorResponse])
async def list_visitors(
    request: Request,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    return await visitor_service.get_visitors(
        request.app.state.db_pool, limit, offset
    )


@router.post(
    "", response_model=VisitorResponse, status_code=201
)
async def create_visitor(data: VisitorCreate, request: Request):
    try:
        return await visitor_service.create_visitor(
            request.app.state.db_pool, data.model_dump()
        )
    except ForeignKeyViolation:
        raise HTTPException(
            status_code=404,
            detail="The specified resident or security guard does not exist.",
        )


@router.get("/{visitor_id}", response_model=VisitorResponse)
async def read_visitor(visitor_id: int, request: Request):
    visitor = await visitor_service.get_visitor(
        request.app.state.db_pool, visitor_id
    )
    if visitor is None:
        raise HTTPException(status_code=404, detail="Visitor record not found.")
    return visitor


@router.put("/{visitor_id}/approval", response_model=VisitorResponse)
async def update_visitor_approval(
    visitor_id: int,
    data: VisitorApprovalUpdate,
    request: Request,
):
    visitor = await visitor_service.update_visitor_approval(
        request.app.state.db_pool,
        visitor_id,
        data.approval_status,
    )
    if visitor is None:
        raise HTTPException(
            status_code=409,
            detail="Visitor not found or already checked out.",
        )
    return visitor


@router.post("/{visitor_id}/checkout", response_model=VisitorResponse)
async def checkout_visitor(visitor_id: int, request: Request):
    visitor = await visitor_service.checkout_visitor(
        request.app.state.db_pool, visitor_id
    )
    if visitor is None:
        raise HTTPException(
            status_code=409,
            detail="Visitor must exist, be approved and not already checked out.",
        )
    return visitor
