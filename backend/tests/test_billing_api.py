from datetime import date
from decimal import Decimal
from uuid import uuid4

import psycopg
from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app


def test_maintenance_bill_and_payment_workflow():
    suffix = uuid4().hex[:10]
    apartment_id = None
    bill_id = None
    payment_ids = []

    with TestClient(app) as client:
        try:
            apartment_response = client.post(
                "/api/v1/apartments",
                json={
                    "building_name": f"Billing Test {suffix}",
                    "flat_number": f"B-{suffix}",
                    "floor_number": 1,
                },
            )
            assert apartment_response.status_code == 201
            apartment_id = apartment_response.json()["apartment_id"]

            bill_payload = {
                "apartment_id": apartment_id,
                "billing_month": "2099-01-01",
                "amount": "2000.00",
                "due_date": "2099-01-15",
            }

            created_bill = client.post(
                "/api/v1/maintenance-bills", json=bill_payload
            )
            assert created_bill.status_code == 201
            bill = created_bill.json()
            bill_id = bill["bill_id"]
            assert bill["bill_status"] == "Unpaid"
            assert Decimal(bill["outstanding_amount"]) == Decimal("2000.00")

            duplicate_bill = client.post(
                "/api/v1/maintenance-bills", json=bill_payload
            )
            assert duplicate_bill.status_code == 409

            partial_payment = client.post(
                "/api/v1/payments",
                json={
                    "bill_id": bill_id,
                    "amount": "750.00",
                    "payment_method": "UPI",
                    "transaction_reference": f"TXN-{suffix}-1",
                },
            )
            assert partial_payment.status_code == 201
            payment_ids.append(partial_payment.json()["payment_id"])

            bill_detail = client.get(f"/api/v1/maintenance-bills/{bill_id}")
            assert bill_detail.status_code == 200
            assert bill_detail.json()["bill_status"] == "Partially Paid"
            assert Decimal(bill_detail.json()["paid_amount"]) == Decimal("750.00")
            assert Decimal(bill_detail.json()["outstanding_amount"]) == Decimal("1250.00")

            overpayment = client.post(
                "/api/v1/payments",
                json={
                    "bill_id": bill_id,
                    "amount": "1300.00",
                    "payment_method": "UPI",
                    "transaction_reference": f"TXN-{suffix}-2",
                },
            )
            assert overpayment.status_code == 409

            final_payment = client.post(
                "/api/v1/payments",
                json={
                    "bill_id": bill_id,
                    "amount": "1250.00",
                    "payment_method": "Card",
                    "transaction_reference": f"TXN-{suffix}-3",
                },
            )
            assert final_payment.status_code == 201
            payment_ids.append(final_payment.json()["payment_id"])

            paid_bill = client.get(f"/api/v1/maintenance-bills/{bill_id}")
            assert paid_bill.json()["bill_status"] == "Paid"
            assert Decimal(paid_bill.json()["outstanding_amount"]) == Decimal("0")

            assert client.get("/api/v1/maintenance-bills").status_code == 200
            assert client.get("/api/v1/payments").status_code == 200

            payment_id = payment_ids[0]
            assert client.get(f"/api/v1/payments/{payment_id}").status_code == 200

            blocked_delete = client.delete(
                f"/api/v1/maintenance-bills/{bill_id}"
            )
            assert blocked_delete.status_code == 409

        finally:
            # Remove only records created by this test.
            if payment_ids or bill_id is not None:
                with psycopg.connect(settings.database_conninfo) as conn:
                    with conn.cursor() as cursor:
                        if bill_id is not None:
                            cursor.execute(
                                "DELETE FROM payments WHERE bill_id = %s",
                                (bill_id,),
                            )
                            cursor.execute(
                                "DELETE FROM maintenance_bills WHERE bill_id = %s",
                                (bill_id,),
                            )
            if apartment_id is not None:
                client.delete(f"/api/v1/apartments/{apartment_id}")


def test_payment_rejects_missing_bill():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/payments",
            json={
                "bill_id": 999999999,
                "amount": "100.00",
                "payment_method": "Cash",
            },
        )
        assert response.status_code == 404


def test_payment_rejects_invalid_method():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/payments",
            json={
                "bill_id": 1,
                "amount": "100.00",
                "payment_method": "Cheque",
            },
        )
        assert response.status_code == 422
