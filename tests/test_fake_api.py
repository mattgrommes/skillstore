"""Tests for fake gym API."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from skillstore.fake_api import reset_bookings
from skillstore.fake_api import router as fake_api_router

# Create a test-only app with fake API enabled
_test_app = FastAPI()
_test_app.include_router(fake_api_router)


@pytest.fixture
def client() -> TestClient:
    """Create a test client with reset state."""
    reset_bookings()
    return TestClient(_test_app)


class TestClassesEndpoint:
    """Tests for GET /api/classes."""

    def test_list_all_classes(self, client: TestClient) -> None:
        """List all classes returns full schedule."""
        response = client.get("/api/classes")
        assert response.status_code == 200
        data = response.json()
        assert "classes" in data
        assert len(data["classes"]) == 5

    def test_filter_by_day(self, client: TestClient) -> None:
        """Filter classes by day."""
        response = client.get("/api/classes?day=Monday")
        assert response.status_code == 200
        classes = response.json()["classes"]
        for c in classes:
            assert "Monday" in c["days"]

    def test_filter_by_type(self, client: TestClient) -> None:
        """Filter classes by type."""
        response = client.get("/api/classes?type=yoga")
        assert response.status_code == 200
        classes = response.json()["classes"]
        assert len(classes) == 2
        for c in classes:
            assert c["type"] == "yoga"

    def test_filter_by_day_and_type(self, client: TestClient) -> None:
        """Filter by both day and type."""
        response = client.get("/api/classes?day=Tuesday&type=yoga")
        assert response.status_code == 200
        classes = response.json()["classes"]
        assert len(classes) == 1
        assert classes[0]["id"] == "yoga-102"


class TestBookingsEndpoint:
    """Tests for /api/bookings endpoints."""

    def test_create_booking(self, client: TestClient) -> None:
        """Create a booking succeeds."""
        response = client.post(
            "/api/bookings",
            json={"class_id": "yoga-101", "date": "2024-01-15"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "confirmed"
        assert data["booking_id"].startswith("bk-")
        assert data["class_info"]["name"] == "Morning Yoga"

    def test_create_booking_invalid_class(self, client: TestClient) -> None:
        """Booking unknown class fails."""
        response = client.post(
            "/api/bookings",
            json={"class_id": "nonexistent", "date": "2024-01-15"},
        )
        assert response.status_code == 400

    def test_class_full_returns_409(self, client: TestClient) -> None:
        """Booking a full class returns 409 Conflict."""
        # spin-201 has 3 spots
        for _ in range(3):
            resp = client.post(
                "/api/bookings",
                json={"class_id": "spin-201", "date": "2024-01-15"},
            )
            assert resp.status_code == 200

        # 4th booking should fail
        response = client.post(
            "/api/bookings",
            json={"class_id": "spin-201", "date": "2024-01-15"},
        )
        assert response.status_code == 409
        assert "full" in response.json()["detail"].lower()

    def test_list_bookings(self, client: TestClient) -> None:
        """List bookings returns created bookings."""
        # Create a booking first
        create_resp = client.post(
            "/api/bookings",
            json={"class_id": "spin-201", "date": "2024-01-20"},
        )
        booking_id = create_resp.json()["booking_id"]

        # List should include it
        response = client.get("/api/bookings")
        assert response.status_code == 200
        bookings = response.json()["bookings"]
        ids = [b["booking_id"] for b in bookings]
        assert booking_id in ids

    def test_cancel_booking(self, client: TestClient) -> None:
        """Cancel a booking succeeds."""
        # Create a booking
        create_resp = client.post(
            "/api/bookings",
            json={"class_id": "cardio-401", "date": "2024-01-25"},
        )
        booking_id = create_resp.json()["booking_id"]

        # Cancel it
        response = client.delete(f"/api/bookings/{booking_id}")
        assert response.status_code == 200
        assert response.json()["status"] == "cancelled"

    def test_cancel_nonexistent_booking(self, client: TestClient) -> None:
        """Cancel unknown booking fails."""
        response = client.delete("/api/bookings/bk-notreal")
        assert response.status_code == 404
