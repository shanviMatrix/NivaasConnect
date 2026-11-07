from fastapi import APIRouter

from app.api.v1.apartments import router as apartments_router
from app.api.v1.complaints import router as complaints_router
from app.api.v1.facilities import router as facilities_router
from app.api.v1.facility_bookings import router as facility_bookings_router
from app.api.v1.health import router as health_router
from app.api.v1.maintenance_bills import router as maintenance_bills_router
from app.api.v1.payments import router as payments_router
from app.api.v1.residents import router as residents_router
from app.api.v1.security_guards import router as security_guards_router
from app.api.v1.society_events import router as society_events_router
from app.api.v1.vendors import router as vendors_router
from app.api.v1.visitors import router as visitors_router

api_router = APIRouter()

for resource_router in (
    health_router,
    apartments_router,
    residents_router,
    vendors_router,
    security_guards_router,
    maintenance_bills_router,
    payments_router,
    complaints_router,
    visitors_router,
    facilities_router,
    facility_bookings_router,
    society_events_router,
):
    api_router.include_router(resource_router)
