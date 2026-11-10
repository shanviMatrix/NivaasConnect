from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


def test_apartment_and_resident_crud():
    suffix = uuid4().hex[:10]
    apartment_id = None
    resident_id = None

    with TestClient(app) as client:
        try:
            apartment_response = client.post(
                "/api/v1/apartments",
                json={
                    "building_name": f"Test Building {suffix}",
                    "flat_number": f"T-{suffix}",
                    "floor_number": 2,
                },
            )

            assert apartment_response.status_code == 201
            apartment = apartment_response.json()
            apartment_id = apartment["apartment_id"]

            assert apartment["floor_number"] == 2

            duplicate_apartment = client.post(
                "/api/v1/apartments",
                json={
                    "building_name": apartment["building_name"],
                    "flat_number": apartment["flat_number"],
                    "floor_number": 2,
                },
            )
            assert duplicate_apartment.status_code == 409

            resident_response = client.post(
                "/api/v1/residents",
                json={
                    "full_name": "Test Resident",
                    "email": f"{suffix}@example.com",
                    "phone": "9876543210",
                    "apartment_id": apartment_id,
                },
            )

            assert resident_response.status_code == 201
            resident = resident_response.json()
            resident_id = resident["resident_id"]

            resident_detail = client.get(
                f"/api/v1/residents/{resident_id}"
            )
            assert resident_detail.status_code == 200
            assert resident_detail.json()["building_name"] == apartment["building_name"]

            duplicate_resident = client.post(
                "/api/v1/residents",
                json={
                    "full_name": "Duplicate Resident",
                    "email": f"{suffix}@example.com",
                    "apartment_id": apartment_id,
                },
            )
            assert duplicate_resident.status_code == 409

            invalid_resident = client.post(
                "/api/v1/residents",
                json={
                    "full_name": "Invalid Resident",
                    "email": f"invalid-{suffix}@example.com",
                    "apartment_id": 999999999,
                },
            )
            assert invalid_resident.status_code == 404

            blocked_delete = client.delete(
                f"/api/v1/apartments/{apartment_id}"
            )
            assert blocked_delete.status_code == 409

            updated_resident = client.put(
                f"/api/v1/residents/{resident_id}",
                json={
                    "full_name": "Updated Test Resident",
                    "email": f"{suffix}@example.com",
                    "phone": None,
                    "apartment_id": apartment_id,
                },
            )
            assert updated_resident.status_code == 200
            assert updated_resident.json()["full_name"] == "Updated Test Resident"

            updated_apartment = client.put(
                f"/api/v1/apartments/{apartment_id}",
                json={
                    "building_name": apartment["building_name"],
                    "flat_number": apartment["flat_number"],
                    "floor_number": 3,
                },
            )
            assert updated_apartment.status_code == 200
            assert updated_apartment.json()["floor_number"] == 3

            assert client.get("/api/v1/apartments").status_code == 200
            assert client.get("/api/v1/residents").status_code == 200

        finally:
            if resident_id is not None:
                client.delete(f"/api/v1/residents/{resident_id}")

            if apartment_id is not None:
                client.delete(f"/api/v1/apartments/{apartment_id}")
