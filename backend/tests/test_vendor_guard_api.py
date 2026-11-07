from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


def test_vendor_crud():
    suffix = uuid4().hex[:10]
    vendor_id = None

    with TestClient(app) as client:
        try:
            payload = {
                "vendor_name": f"Test Vendor {suffix}",
                "service_category": "Plumbing",
                "phone": "98765" + suffix[:5],
                "email": f"{suffix}@vendor.example",
            }

            created = client.post("/api/v1/vendors", json=payload)
            assert created.status_code == 201
            vendor = created.json()
            vendor_id = vendor["vendor_id"]
            assert vendor["is_active"] is True

            duplicate = client.post("/api/v1/vendors", json=payload)
            assert duplicate.status_code == 409

            fetched = client.get(f"/api/v1/vendors/{vendor_id}")
            assert fetched.status_code == 200

            updated_payload = {
                **payload,
                "vendor_name": f"Updated Vendor {suffix}",
                "is_active": False,
            }
            updated = client.put(
                f"/api/v1/vendors/{vendor_id}", json=updated_payload
            )
            assert updated.status_code == 200
            assert updated.json()["is_active"] is False

            assert client.get("/api/v1/vendors").status_code == 200

            missing = client.get("/api/v1/vendors/999999999")
            assert missing.status_code == 404

        finally:
            if vendor_id is not None:
                client.delete(f"/api/v1/vendors/{vendor_id}")


def test_security_guard_crud():
    suffix = uuid4().hex[:10]
    guard_id = None

    with TestClient(app) as client:
        try:
            payload = {
                "full_name": f"Test Guard {suffix}",
                "phone": "8" + suffix,
                "shift_name": "Night",
            }

            created = client.post("/api/v1/security-guards", json=payload)
            assert created.status_code == 201
            guard = created.json()
            guard_id = guard["guard_id"]
            assert guard["is_active"] is True

            duplicate = client.post("/api/v1/security-guards", json=payload)
            assert duplicate.status_code == 409

            invalid_shift = client.post(
                "/api/v1/security-guards",
                json={**payload, "phone": "7" + suffix, "shift_name": "Afternoon"},
            )
            assert invalid_shift.status_code == 422

            fetched = client.get(f"/api/v1/security-guards/{guard_id}")
            assert fetched.status_code == 200

            updated_payload = {
                **payload,
                "full_name": f"Updated Guard {suffix}",
                "shift_name": "Morning",
                "is_active": False,
            }
            updated = client.put(
                f"/api/v1/security-guards/{guard_id}",
                json=updated_payload,
            )
            assert updated.status_code == 200
            assert updated.json()["shift_name"] == "Morning"
            assert updated.json()["is_active"] is False

            assert client.get("/api/v1/security-guards").status_code == 200

            missing = client.get("/api/v1/security-guards/999999999")
            assert missing.status_code == 404

        finally:
            if guard_id is not None:
                client.delete(f"/api/v1/security-guards/{guard_id}")
