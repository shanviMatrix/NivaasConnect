

import pytest

from app.api.dependencies import get_current_user
from app.main import app


@pytest.fixture(autouse=True)
def admin_auth_for_legacy_tests():
    app.dependency_overrides[get_current_user] = lambda: {
        "account_id": 1,
        "username": "admin",
        "role": "Admin",
        "resident_id": None,
        "guard_id": None,
        "is_active": True,
    }
    yield
    app.dependency_overrides.pop(get_current_user, None)
