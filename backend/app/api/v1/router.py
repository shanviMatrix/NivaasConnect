from fastapi import APIRouter

from app.api.v1.apartments import router as apartments_router
from app.api.v1.health import router as health_router
from app.api.v1.residents import router as residents_router
from app.api.v1.security_guards import router as security_guards_router
from app.api.v1.vendors import router as vendors_router

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(apartments_router)
api_router.include_router(residents_router)
api_router.include_router(vendors_router)
api_router.include_router(security_guards_router)
