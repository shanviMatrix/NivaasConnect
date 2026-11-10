from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


def test_complaint_crud_and_resolution():
    suffix = uuid4().hex[:10]
    apartment_id = resident_id = complaint_id = None

    with TestClient(app) as client:
        try:
            apartment = client.post(
                "/api/v1/apartments",
                json={
                    "building_name": f"Complaint Test {suffix}",
                    "flat_number": f"C-{suffix}",
                },
            )
            assert apartment.status_code == 201
            apartment_id = apartment.json()["apartment_id"]

            resident = client.post(
                "/api/v1/residents",
                json={
                    "full_name": "Complaint Test Resident",
                    "email": f"{suffix}@complaint.example",
                    "apartment_id": apartment_id,
                },
            )
            assert resident.status_code == 201
            resident_id = resident.json()["resident_id"]

            payload = {
                "resident_id": resident_id,
                "title": f"Water leakage {suffix}",
                "description": "Water leakage in the bathroom.",
                "category": "Plumbing",
                "priority": "High",
            }

            created = client.post("/api/v1/complaints", json=payload)
            assert created.status_code == 201
            complaint = created.json()
            complaint_id = complaint["complaint_id"]
            assert complaint["complaint_status"] == "Open"
            assert complaint["resolved_at"] is None

            updated = client.put(
                f"/api/v1/complaints/{complaint_id}",
                json={**payload, "complaint_status": "In Progress"},
            )
            assert updated.status_code == 200
            assert updated.json()["complaint_status"] == "In Progress"

            resolved = client.put(
                f"/api/v1/complaints/{complaint_id}",
                json={**payload, "complaint_status": "Resolved"},
            )
            assert resolved.status_code == 200
            assert resolved.json()["resolved_at"] is not None

            fetched = client.get(f"/api/v1/complaints/{complaint_id}")
            assert fetched.status_code == 200
            assert client.get("/api/v1/complaints").status_code == 200

            invalid_category = client.post(
                "/api/v1/complaints",
                json={**payload, "category": "Gardening"},
            )
            assert invalid_category.status_code == 422

        finally:
            if complaint_id is not None:
                client.delete(f"/api/v1/complaints/{complaint_id}")
            if resident_id is not None:
                client.delete(f"/api/v1/residents/{resident_id}")
            if apartment_id is not None:
                client.delete(f"/api/v1/apartments/{apartment_id}")


def test_visitor_approval_and_checkout():
    suffix = uuid4().hex[:10]
    apartment_id = resident_id = guard_id = visitor_id = None

    with TestClient(app) as client:
        try:
            apartment = client.post(
                "/api/v1/apartments",
                json={
                    "building_name": f"Visitor Test {suffix}",
                    "flat_number": f"V-{suffix}",
                },
            )
            assert apartment.status_code == 201
            apartment_id = apartment.json()["apartment_id"]

            resident = client.post(
                "/api/v1/residents",
                json={
                    "full_name": "Visitor Test Resident",
                    "email": f"{suffix}@visitor.example",
                    "apartment_id": apartment_id,
                },
            )
            assert resident.status_code == 201
            resident_id = resident.json()["resident_id"]

            guard = client.post(
                "/api/v1/security-guards",
                json={
                    "full_name": f"Test Guard {suffix}",
                    "phone": "8" + suffix,
                    "shift_name": "Night",
                },
            )
            assert guard.status_code == 201
            guard_id = guard.json()["guard_id"]

            payload = {
                "resident_id": resident_id,
                "guard_id": guard_id,
                "visitor_name": "Test Visitor",
                "visitor_phone": "9876543210",
                "purpose": "Meeting resident",
            }

            created = client.post("/api/v1/visitors", json=payload)
            assert created.status_code == 201
            visitor = created.json()
            visitor_id = visitor["visitor_id"]
            assert visitor["approval_status"] == "Pending"
            assert visitor["exit_time"] is None

            denied = client.put(
                f"/api/v1/visitors/{visitor_id}/approval",
                json={"approval_status": "Denied"},
            )
            assert denied.status_code == 200

            denied_checkout = client.post(
                f"/api/v1/visitors/{visitor_id}/checkout"
            )
            assert denied_checkout.status_code == 409

            approved = client.put(
                f"/api/v1/visitors/{visitor_id}/approval",
                json={"approval_status": "Approved"},
            )
            assert approved.status_code == 200

            checkout = client.post(
                f"/api/v1/visitors/{visitor_id}/checkout"
            )
            assert checkout.status_code == 200
            assert checkout.json()["exit_time"] is not None

            repeated_checkout = client.post(
                f"/api/v1/visitors/{visitor_id}/checkout"
            )
            assert repeated_checkout.status_code == 409

            assert client.get("/api/v1/visitors").status_code == 200
            assert client.get(f"/api/v1/visitors/{visitor_id}").status_code == 200

        finally:
            if visitor_id is not None:
                with __import__("psycopg").connect(
                    __import__("app.core.config", fromlist=["settings"]).settings.database_conninfo
                ) as conn:
                    with conn.cursor() as cursor:
                        cursor.execute(
                            "DELETE FROM visitor_logs WHERE visitor_id = %s",
                            (visitor_id,),
                        )
            if guard_id is not None:
                client.delete(f"/api/v1/security-guards/{guard_id}")
            if resident_id is not None:
                client.delete(f"/api/v1/residents/{resident_id}")
            if apartment_id is not None:
                client.delete(f"/api/v1/apartments/{apartment_id}")
