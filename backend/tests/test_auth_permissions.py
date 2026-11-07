from fastapi.testclient import TestClient

from app.api.dependencies import get_current_user
from app.main import app


def test_protected_route_rejects_unauthenticated_request():
    app.dependency_overrides.pop(get_current_user, None)

    with TestClient(app) as client:
        response = client.get("/api/v1/apartments")

    assert response.status_code == 401


def test_protected_route_rejects_wrong_role():
    app.dependency_overrides[get_current_user] = lambda: {
        "account_id": 2,
        "username": "resident_test",
        "role": "Resident",
        "resident_id": 1,
        "guard_id": None,
        "is_active": True,
    }

    with TestClient(app) as client:
        response = client.get("/api/v1/apartments")

    assert response.status_code == 403
