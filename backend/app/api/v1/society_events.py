from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response, status
from psycopg.errors import ForeignKeyViolation

from app.schemas.society_event import (
    SocietyEventCreate,
    SocietyEventResponse,
    SocietyEventUpdate,
)
from app.services import society_event_service

from app.api.dependencies import authorize_resource_access

router = APIRouter(dependencies=[Depends(authorize_resource_access)], prefix="/society-events", tags=["Society Events"])


@router.get("", response_model=list[SocietyEventResponse])
async def list_events(
    request: Request,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    return await society_event_service.get_events(
        request.app.state.db_pool, limit, offset
    )


@router.post("", response_model=SocietyEventResponse, status_code=201)
async def create_event(data: SocietyEventCreate, request: Request):
    try:
        return await society_event_service.create_event(
            request.app.state.db_pool, data.model_dump()
        )
    except ForeignKeyViolation:
        raise HTTPException(status_code=404, detail="The specified resident does not exist.")


@router.get("/{event_id}", response_model=SocietyEventResponse)
async def read_event(event_id: int, request: Request):
    event = await society_event_service.get_event(request.app.state.db_pool, event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Society event not found.")
    return event


@router.put("/{event_id}", response_model=SocietyEventResponse)
async def edit_event(event_id: int, data: SocietyEventUpdate, request: Request):
    try:
        event = await society_event_service.update_event(
            request.app.state.db_pool, event_id, data.model_dump()
        )
    except ForeignKeyViolation:
        raise HTTPException(status_code=404, detail="The specified resident does not exist.")

    if event is None:
        raise HTTPException(status_code=404, detail="Society event not found.")
    return event


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_event(event_id: int, request: Request):
    deleted = await society_event_service.delete_event(request.app.state.db_pool, event_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Society event not found.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
