import pytest
from pydantic import ValidationError

from app.schemas.apartment import ApartmentCreate
from app.schemas.resident import ResidentCreate


def test_valid_apartment():
    apartment = ApartmentCreate(
        building_name="Tower A",
        flat_number="A-101",
        floor_number=1,
    )

    assert apartment.building_name == "Tower A"
    assert apartment.flat_number == "A-101"


def test_apartment_rejects_negative_floor():
    with pytest.raises(ValidationError):
        ApartmentCreate(
            building_name="Tower A",
            flat_number="A-102",
            floor_number=-1,
        )


def test_apartment_rejects_empty_building_name():
    with pytest.raises(ValidationError):
        ApartmentCreate(
            building_name="   ",
            flat_number="A-102",
        )


def test_valid_resident():
    resident = ResidentCreate(
        full_name="Test Resident",
        email="TEST@example.com",
        phone="9876543210",
        apartment_id=1,
    )

    assert resident.email == "test@example.com"


def test_resident_rejects_invalid_email():
    with pytest.raises(ValidationError):
        ResidentCreate(
            full_name="Test Resident",
            email="invalid-email",
            apartment_id=1,
        )


def test_resident_rejects_invalid_apartment_id():
    with pytest.raises(ValidationError):
        ResidentCreate(
            full_name="Test Resident",
            email="test@example.com",
            apartment_id=0,
        )
