from fastapi import APIRouter, Depends, HTTPException, Query, Request

from app.api.dependencies import require_roles
from app.schemas.visitor import VisitorApprovalUpdate, VisitorCreate, VisitorResponse
from app.services import visitor_service

router = APIRouter(prefix="/visitors", tags=["Visitors"])


@router.get("", response_model=list[VisitorResponse])
async def list_visitors(
    request: Request,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    user: dict = Depends(require_roles("Admin", "Security")),
):
    guard_id = user["guard_id"] if user["role"] == "Security" else None
    return await visitor_service.get_visitors(
        request.app.state.db_pool, limit, offset, guard_id
    )


@router.post("", response_model=VisitorResponse, status_code=201)
async def create_visitor(
    data: VisitorCreate,
    request: Request,
    user: dict = Depends(require_roles("Admin", "Security")),
):
    payload = data.model_dump()
    if user["role"] == "Security":
        payload["guard_id"] = user["guard_id"]
    elif payload["guard_id"] is None:
        raise HTTPException(status_code=422, detail="guard_id is required for Admin.")
    try:
        return await visitor_service.create_visitor(request.app.state.db_pool, payload)
    except Exception as exc:
        from psycopg.errors import ForeignKeyViolation
        if isinstance(exc, ForeignKeyViolation):
            raise HTTPException(status_code=404, detail="The specified resident or security guard does not exist.")
        raise


@router.get("/{visitor_id}", response_model=VisitorResponse)
async def read_visitor(
    visitor_id: int,
    request: Request,
    user: dict = Depends(require_roles("Admin", "Security")),
):
    guard_id = user["guard_id"] if user["role"] == "Security" else None
    visitor = await visitor_service.get_visitor(request.app.state.db_pool, visitor_id, guard_id)
    if visitor is None:
        raise HTTPException(status_code=404, detail="Visitor record not found.")
    return visitor


@router.put("/{visitor_id}/approval", response_model=VisitorResponse)
async def update_visitor_approval(
    visitor_id: int,
    data: VisitorApprovalUpdate,
    request: Request,
    user: dict = Depends(require_roles("Admin", "Security")),
):
    guard_id = user["guard_id"] if user["role"] == "Security" else None
    visitor = await visitor_service.update_visitor_approval(
        request.app.state.db_pool, visitor_id, data.approval_status, guard_id
    )
    if visitor is None:
        raise HTTPException(status_code=409, detail="Visitor not found, not assigned to this guard, or already checked out.")
    return visitor


@router.post("/{visitor_id}/checkout", response_model=VisitorResponse)
async def checkout_visitor(
    visitor_id: int,
    request: Request,
    user: dict = Depends(require_roles("Admin", "Security")),
):
    guard_id = user["guard_id"] if user["role"] == "Security" else None
    visitor = await visitor_service.checkout_visitor(
        request.app.state.db_pool, visitor_id, guard_id
    )
    if visitor is None:
        raise HTTPException(status_code=409, detail="Visitor must be approved, assigned to this guard, and not already checked out.")
    return visitor
