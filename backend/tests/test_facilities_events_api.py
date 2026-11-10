from datetime import datetime, timedelta, timezone
from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


def create_test_resident(client, suffix):
    apartment = client.post(
        "/api/v1/apartments",
        json={
            "building_name": f"Facility Test {suffix}",
            "flat_number": f"F-{suffix}",
        },
    )
    assert apartment.status_code == 201
    apartment_id = apartment.json()["apartment_id"]

    resident = client.post(
        "/api/v1/residents",
        json={
            "full_name": "Facility Test Resident",
            "email": f"{suffix}@facility.example",
            "apartment_id": apartment_id,
        },
    )
    assert resident.status_code == 201
    return apartment_id, resident.json()["resident_id"]


def test_facility_booking_workflow():
    suffix = uuid4().hex[:10]
    apartment_id = resident_id = facility_id = None

    with TestClient(app) as client:
        try:
            apartment_id, resident_id = create_test_resident(client, suffix)

            facility = client.post(
                "/api/v1/facilities",
                json={
                    "facility_name": f"Test Hall {suffix}",
                    "location_description": "Ground floor",
                    "capacity": 100,
                    "booking_fee": "500.00",
                },
            )
            assert facility.status_code == 201
            facility_id = facility.json()["facility_id"]

            assert client.get("/api/v1/facilities").status_code == 200
            assert client.get(f"/api/v1/facilities/{facility_id}").status_code == 200

            start = datetime.now(timezone.utc) + timedelta(days=3)
            end = start + timedelta(hours=2)
            payload = {
                "facility_id": facility_id,
                "resident_id": resident_id,
                "start_time": start.isoformat(),
                "end_time": end.isoformat(),
            }

            booking = client.post("/api/v1/facility-bookings", json=payload)
            assert booking.status_code == 201
            booking_id = booking.json()["booking_id"]
            assert booking.json()["booking_status"] == "Pending"

            overlap = {
                **payload,
                "start_time": (start + timedelta(minutes=30)).isoformat(),
                "end_time": (end + timedelta(minutes=30)).isoformat(),
            }
            conflict = client.post("/api/v1/facility-bookings", json=overlap)
            assert conflict.status_code == 409

            approved = client.put(
                f"/api/v1/facility-bookings/{booking_id}/status",
                json={"booking_status": "Approved"},
            )
            assert approved.status_code == 200
            assert approved.json()["booking_status"] == "Approved"

            assert client.get("/api/v1/facility-bookings").status_code == 200
            assert client.get(f"/api/v1/facility-bookings/{booking_id}").status_code == 200

            invalid_time = client.post(
                "/api/v1/facility-bookings",
                json={**payload, "end_time": start.isoformat()},
            )
            assert invalid_time.status_code == 422

        finally:
            # Remove dependent bookings before deleting the facility/resident.
            if facility_id is not None:
                from app.core.config import settings
                import psycopg

                with psycopg.connect(settings.database_conninfo) as conn:
                    with conn.cursor() as cur:
                        cur.execute(
                            "DELETE FROM facility_bookings WHERE facility_id = %s",
                            (facility_id,),
                        )
                client.delete(f"/api/v1/facilities/{facility_id}")

            if resident_id is not None:
                client.delete(f"/api/v1/residents/{resident_id}")
            if apartment_id is not None:
                client.delete(f"/api/v1/apartments/{apartment_id}")


def test_society_event_crud():
    suffix = uuid4().hex[:10]
    apartment_id = resident_id = event_id = None

    with TestClient(app) as client:
        try:
            apartment_id, resident_id = create_test_resident(client, suffix)

            start = datetime.now(timezone.utc) + timedelta(days=5)
            end = start + timedelta(hours=3)
            payload = {
                "event_title": f"Community Meetup {suffix}",
                "description": "Monthly society gathering",
                "venue": "Community Hall",
                "start_time": start.isoformat(),
                "end_time": end.isoformat(),
                "created_by": resident_id,
            }

            created = client.post("/api/v1/society-events", json=payload)
            assert created.status_code == 201
            event_id = created.json()["event_id"]
            assert created.json()["event_status"] == "Planned"

            updated = client.put(
                f"/api/v1/society-events/{event_id}",
                json={**payload, "event_status": "Ongoing"},
            )
            assert updated.status_code == 200
            assert updated.json()["event_status"] == "Ongoing"

            assert client.get("/api/v1/society-events").status_code == 200
            assert client.get(f"/api/v1/society-events/{event_id}").status_code == 200

            deleted = client.delete(f"/api/v1/society-events/{event_id}")
            assert deleted.status_code == 204
            event_id = None

            invalid_time = client.post(
                "/api/v1/society-events",
                json={**payload, "end_time": start.isoformat()},
            )
            assert invalid_time.status_code == 422

        finally:
            if event_id is not None:
                client.delete(f"/api/v1/society-events/{event_id}")
            if resident_id is not None:
                client.delete(f"/api/v1/residents/{resident_id}")
            if apartment_id is not None:
                client.delete(f"/api/v1/apartments/{apartment_id}")
