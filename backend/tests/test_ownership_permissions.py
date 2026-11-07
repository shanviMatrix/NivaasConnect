
from datetime import datetime, timedelta, timezone
from uuid import uuid4

import psycopg

from app.core.config import settings
from fastapi.testclient import TestClient

from app.api.dependencies import get_current_user
from app.main import app


def set_user(role, resident_id=None, guard_id=None):
    app.dependency_overrides[get_current_user] = lambda: {
        "account_id": 20,
        "username": "ownership_test",
        "role": role,
        "resident_id": resident_id,
        "guard_id": guard_id,
        "is_active": True,
    }


def test_resident_can_read_bills_and_payments():
    set_user("Resident", resident_id=1)
    with TestClient(app) as client:
        assert client.get("/api/v1/maintenance-bills").status_code == 200
        assert client.get("/api/v1/payments").status_code == 200


def test_resident_cannot_create_bills_or_payments():
    set_user("Resident", resident_id=1)
    with TestClient(app) as client:
        assert client.post("/api/v1/maintenance-bills", json={}).status_code == 403
        assert client.post("/api/v1/payments", json={}).status_code == 403


def test_security_can_access_visitor_logs():
    set_user("Security", guard_id=1)
    with TestClient(app) as client:
        assert client.get("/api/v1/visitors").status_code == 200


def test_resident_cannot_access_visitor_logs():
    set_user("Resident", resident_id=1)
    with TestClient(app) as client:
        assert client.get("/api/v1/visitors").status_code == 403


def test_security_cannot_manage_billing_or_complaints():
    set_user("Security", guard_id=1)
    with TestClient(app) as client:
        assert client.get("/api/v1/maintenance-bills").status_code == 403
        assert client.get("/api/v1/payments").status_code == 403
        assert client.get("/api/v1/complaints").status_code == 403



def test_resident_cannot_access_another_residents_records():
    suffix = uuid4().hex[:10]
    apartment_ids = []
    resident_ids = []
    bill_ids = []
    facility_id = None

    with TestClient(app) as client:
        try:
            # Create two independent apartments and residents as Admin.
            for index in range(2):
                apartment = client.post(
                    "/api/v1/apartments",
                    json={
                        "building_name": f"Isolation {suffix}",
                        "flat_number": f"{index}-{suffix}",
                    },
                )
                assert apartment.status_code == 201
                apartment_ids.append(apartment.json()["apartment_id"])

                resident = client.post(
                    "/api/v1/residents",
                    json={
                        "full_name": f"Isolation Resident {index}",
                        "email": f"{index}-{suffix}@isolation.example",
                        "apartment_id": apartment_ids[-1],
                    },
                )
                assert resident.status_code == 201
                resident_ids.append(resident.json()["resident_id"])

            # Create one bill, payment and complaint for each resident.
            payment_ids = []
            complaint_ids = []

            for index in range(2):
                bill = client.post(
                    "/api/v1/maintenance-bills",
                    json={
                        "apartment_id": apartment_ids[index],
                        "billing_month": f"2098-0{index + 1}-01",
                        "amount": "1000.00",
                        "due_date": f"2098-0{index + 1}-15",
                    },
                )
                assert bill.status_code == 201
                bill_ids.append(bill.json()["bill_id"])

                payment = client.post(
                    "/api/v1/payments",
                    json={
                        "bill_id": bill_ids[-1],
                        "amount": "250.00",
                        "payment_method": "UPI",
                        "transaction_reference": f"ISO-{suffix}-{index}",
                    },
                )
                assert payment.status_code == 201
                payment_ids.append(payment.json()["payment_id"])

                complaint = client.post(
                    "/api/v1/complaints",
                    json={
                        "resident_id": resident_ids[index],
                        "title": f"Isolation complaint {index} {suffix}",
                        "description": "Ownership isolation test.",
                        "category": "Plumbing",
                        "priority": "Medium",
                    },
                )
                assert complaint.status_code == 201
                complaint_ids.append(complaint.json()["complaint_id"])

            facility = client.post(
                "/api/v1/facilities",
                json={
                    "facility_name": f"Isolation Facility {suffix}",
                    "location_description": "Test area",
                    "capacity": 20,
                    "booking_fee": "100.00",
                },
            )
            assert facility.status_code == 201
            facility_id = facility.json()["facility_id"]

            booking_ids = []
            start = datetime.now(timezone.utc) + timedelta(days=10)

            for index in range(2):
                booking = client.post(
                    "/api/v1/facility-bookings",
                    json={
                        "facility_id": facility_id,
                        "resident_id": resident_ids[index],
                        "start_time": (
                            start + timedelta(days=index * 2)
                        ).isoformat(),
                        "end_time": (
                            start + timedelta(days=index * 2, hours=1)
                        ).isoformat(),
                    },
                )
                assert booking.status_code == 201
                booking_ids.append(booking.json()["booking_id"])

            # Switch identity to Resident A.
            set_user("Resident", resident_id=resident_ids[0])

            for endpoint, own_id, other_id in [
                ("/api/v1/maintenance-bills", bill_ids[0], bill_ids[1]),
                ("/api/v1/payments", payment_ids[0], payment_ids[1]),
                ("/api/v1/complaints", complaint_ids[0], complaint_ids[1]),
                ("/api/v1/facility-bookings", booking_ids[0], booking_ids[1]),
            ]:
                listing = client.get(endpoint)
                assert listing.status_code == 200
                visible_ids = {
                    item[next(
                        key for key in item
                        if key.endswith("_id") and key != "resident_id"
                    )]
                    for item in listing.json()
                }
                assert own_id in visible_ids
                assert other_id not in visible_ids

                assert client.get(f"{endpoint}/{other_id}").status_code == 404
                assert client.get(f"{endpoint}/{own_id}").status_code == 200

        finally:
            set_user("Admin")

            with psycopg.connect(settings.database_conninfo) as conn:
                with conn.cursor() as cursor:
                    if resident_ids:
                        cursor.execute(
                            "DELETE FROM complaints WHERE resident_id = ANY(%s)",
                            (resident_ids,),
                        )
                        cursor.execute(
                            "DELETE FROM facility_bookings WHERE resident_id = ANY(%s)",
                            (resident_ids,),
                        )
                    if bill_ids:
                        cursor.execute(
                            "DELETE FROM payments WHERE bill_id = ANY(%s)",
                            (bill_ids,),
                        )
                        cursor.execute(
                            "DELETE FROM maintenance_bills WHERE bill_id = ANY(%s)",
                            (bill_ids,),
                        )
                    if resident_ids:
                        cursor.execute(
                            "DELETE FROM residents WHERE resident_id = ANY(%s)",
                            (resident_ids,),
                        )
                    if facility_id is not None:
                        cursor.execute(
                            "DELETE FROM facilities WHERE facility_id = %s",
                            (facility_id,),
                        )
                    if apartment_ids:
                        cursor.execute(
                            "DELETE FROM apartments WHERE apartment_id = ANY(%s)",
                            (apartment_ids,),
                        )


def test_security_guard_cannot_access_another_guards_visitors():
    suffix = uuid4().hex[:10]
    apartment_id = resident_id = None
    guard_ids = []
    visitor_ids = []

    with TestClient(app) as client:
        try:
            apartment = client.post(
                "/api/v1/apartments",
                json={
                    "building_name": f"Guard Isolation {suffix}",
                    "flat_number": f"G-{suffix}",
                },
            )
            assert apartment.status_code == 201
            apartment_id = apartment.json()["apartment_id"]

            resident = client.post(
                "/api/v1/residents",
                json={
                    "full_name": "Guard Isolation Resident",
                    "email": f"{suffix}@guard-isolation.example",
                    "apartment_id": apartment_id,
                },
            )
            assert resident.status_code == 201
            resident_id = resident.json()["resident_id"]

            for index in range(2):
                guard = client.post(
                    "/api/v1/security-guards",
                    json={
                        "full_name": f"Isolation Guard {index} {suffix}",
                        "phone": f"7{suffix[:9]}{index}",
                        "shift_name": "Night",
                    },
                )
                assert guard.status_code == 201
                guard_ids.append(guard.json()["guard_id"])

                visitor = client.post(
                    "/api/v1/visitors",
                    json={
                        "resident_id": resident_id,
                        "guard_id": guard_ids[-1],
                        "visitor_name": f"Visitor {index}",
                        "visitor_phone": "9876543210",
                        "purpose": "Ownership isolation test",
                    },
                )
                assert visitor.status_code == 201
                visitor_ids.append(visitor.json()["visitor_id"])

            # Switch identity to Guard A.
            set_user("Security", guard_id=guard_ids[0])

            listing = client.get("/api/v1/visitors")
            assert listing.status_code == 200

            visible_ids = {
                item["visitor_id"] for item in listing.json()
            }
            assert visitor_ids[0] in visible_ids
            assert visitor_ids[1] not in visible_ids

            assert client.get(
                f"/api/v1/visitors/{visitor_ids[0]}"
            ).status_code == 200

            assert client.get(
                f"/api/v1/visitors/{visitor_ids[1]}"
            ).status_code == 404

            assert client.put(
                f"/api/v1/visitors/{visitor_ids[1]}/approval",
                json={"approval_status": "Approved"},
            ).status_code == 409

            assert client.post(
                f"/api/v1/visitors/{visitor_ids[1]}/checkout"
            ).status_code == 409

        finally:
            set_user("Admin")

            with psycopg.connect(settings.database_conninfo) as conn:
                with conn.cursor() as cursor:
                    if visitor_ids:
                        cursor.execute(
                            "DELETE FROM visitor_logs WHERE visitor_id = ANY(%s)",
                            (visitor_ids,),
                        )
                    if resident_id is not None:
                        cursor.execute(
                            "DELETE FROM residents WHERE resident_id = %s",
                            (resident_id,),
                        )
                    if guard_ids:
                        cursor.execute(
                            "DELETE FROM security_guards WHERE guard_id = ANY(%s)",
                            (guard_ids,),
                        )
                    if apartment_id is not None:
                        cursor.execute(
                            "DELETE FROM apartments WHERE apartment_id = %s",
                            (apartment_id,),
                        )
