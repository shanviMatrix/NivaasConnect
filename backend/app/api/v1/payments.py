from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from psycopg.errors import UniqueViolation

from app.api.dependencies import require_roles
from app.schemas.payment import PaymentCreate, PaymentResponse
from app.services import payment_service

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.get("", response_model=list[PaymentResponse])
async def list_payments(
    request: Request,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    user: dict = Depends(require_roles("Admin", "Resident")),
):
    resident_id = user["resident_id"] if user["role"] == "Resident" else None
    return await payment_service.get_payments(
        request.app.state.db_pool, limit, offset, resident_id
    )


@router.post("", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(require_roles("Admin"))])
async def create_payment(data: PaymentCreate, request: Request):
    try:
        return await payment_service.create_payment(
            request.app.state.db_pool, data.model_dump()
        )
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    except UniqueViolation:
        raise HTTPException(status_code=409, detail="This transaction reference already exists.")


@router.get("/{payment_id}", response_model=PaymentResponse)
async def read_payment(
    payment_id: int,
    request: Request,
    user: dict = Depends(require_roles("Admin", "Resident")),
):
    resident_id = user["resident_id"] if user["role"] == "Resident" else None
    payment = await payment_service.get_payment(
        request.app.state.db_pool, payment_id, resident_id
    )
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found.")
    return payment
