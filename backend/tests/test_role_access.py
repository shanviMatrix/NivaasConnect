from fastapi.testclient import TestClient

from app.api.dependencies import get_current_user
from app.main import app


def set_test_user(role: str):
    app.dependency_overrides[get_current_user] = lambda: {
        "account_id": 2,
        "username": "role_test",
        "role": role,
        "resident_id": 1 if role == "Resident" else None,
        "guard_id": 1 if role == "Security" else None,
        "is_active": True,
    }


def test_resident_can_read_shared_information():
    set_test_user("Resident")

    with TestClient(app) as client:
        assert client.get("/api/v1/vendors").status_code == 200
        assert client.get("/api/v1/facilities").status_code == 200
        assert client.get("/api/v1/society-events").status_code == 200


def test_security_can_read_shared_information():
    set_test_user("Security")

    with TestClient(app) as client:
        assert client.get("/api/v1/vendors").status_code == 200
        assert client.get("/api/v1/facilities").status_code == 200
        assert client.get("/api/v1/society-events").status_code == 200


def test_resident_cannot_modify_shared_information():
    set_test_user("Resident")

    with TestClient(app) as client:
        response = client.post(
            "/api/v1/vendors",
            json={
                "vendor_name": "Unauthorized Vendor",
                "service_category": "Cleaning",
            },
        )

    assert response.status_code == 403


def test_resident_cannot_list_all_residents():
    set_test_user("Resident")

    with TestClient(app) as client:
        response = client.get("/api/v1/residents")

    assert response.status_code == 403


def test_security_cannot_list_all_guards():
    set_test_user("Security")

    with TestClient(app) as client:
        response = client.get("/api/v1/security-guards")

    assert response.status_code == 403
