"""Fake gym API endpoints for testing skills.

These endpoints implement the API described in the example skills
(class-schedule and book-appointment) to allow end-to-end testing.
"""

from uuid import uuid4

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

router = APIRouter(prefix="/api", tags=["fake-gym-api"])

# In-memory storage for bookings
_bookings: dict[str, dict] = {}


def reset_bookings() -> None:
    """Reset bookings storage - for testing."""
    _bookings.clear()
    # Reset class availability
    for c in FAKE_CLASSES:
        c.spots_available = _original_spots[c.id]


class GymClass(BaseModel):
    """A gym class in the schedule."""

    id: str
    name: str
    instructor: str
    time: str
    duration_minutes: int
    room: str
    spots_available: int
    days: list[str]
    type: str


class ClassesResponse(BaseModel):
    """Response from GET /api/classes."""

    classes: list[GymClass]


class BookingRequest(BaseModel):
    """Request body for POST /api/bookings."""

    class_id: str
    date: str


class BookingClassInfo(BaseModel):
    """Class info embedded in booking response."""

    name: str
    time: str
    instructor: str


class BookingResponse(BaseModel):
    """Response from POST /api/bookings."""

    booking_id: str
    status: str
    class_info: BookingClassInfo
    date: str


class BookingListItem(BaseModel):
    """A booking in the list response."""

    booking_id: str
    class_id: str
    class_name: str
    date: str
    time: str
    status: str


class BookingsListResponse(BaseModel):
    """Response from GET /api/bookings."""

    bookings: list[BookingListItem]


class CancelResponse(BaseModel):
    """Response from DELETE /api/bookings/{id}."""

    status: str
    refund_status: str


# Fake class schedule data
FAKE_CLASSES: list[GymClass] = [
    GymClass(
        id="yoga-101",
        name="Morning Yoga",
        instructor="Sarah",
        time="07:00",
        duration_minutes=60,
        room="Studio A",
        spots_available=5,
        days=["Monday", "Wednesday", "Friday"],
        type="yoga",
    ),
    GymClass(
        id="yoga-102",
        name="Evening Flow",
        instructor="Mike",
        time="18:00",
        duration_minutes=75,
        room="Studio A",
        spots_available=8,
        days=["Tuesday", "Thursday"],
        type="yoga",
    ),
    GymClass(
        id="spin-201",
        name="Power Spin",
        instructor="Jake",
        time="06:30",
        duration_minutes=45,
        room="Spin Room",
        spots_available=3,
        days=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        type="spinning",
    ),
    GymClass(
        id="strength-301",
        name="Full Body Strength",
        instructor="Emma",
        time="12:00",
        duration_minutes=60,
        room="Weight Room",
        spots_available=10,
        days=["Monday", "Wednesday", "Friday"],
        type="strength",
    ),
    GymClass(
        id="cardio-401",
        name="HIIT Blast",
        instructor="Carlos",
        time="17:30",
        duration_minutes=30,
        room="Studio B",
        spots_available=15,
        days=["Tuesday", "Thursday", "Saturday"],
        type="cardio",
    ),
]

# Index classes by ID for quick lookup
_classes_by_id = {c.id: c for c in FAKE_CLASSES}

# Store original spots for reset
_original_spots = {c.id: c.spots_available for c in FAKE_CLASSES}


@router.get("/classes", response_model=ClassesResponse)
async def list_classes(
    day: str | None = Query(None, description="Filter by day of the week"),
    type: str | None = Query(None, description="Filter by class type"),
) -> ClassesResponse:
    """List gym classes with optional filtering."""
    result = FAKE_CLASSES

    if day:
        day_normalized = day.capitalize()
        result = [c for c in result if day_normalized in c.days]

    if type:
        type_normalized = type.lower()
        result = [c for c in result if c.type == type_normalized]

    return ClassesResponse(classes=result)


@router.post("/bookings", response_model=BookingResponse)
async def create_booking(request: BookingRequest) -> BookingResponse:
    """Create a new class booking."""
    gym_class = _classes_by_id.get(request.class_id)
    if not gym_class:
        raise HTTPException(status_code=400, detail=f"Unknown class_id: {request.class_id}")

    if gym_class.spots_available <= 0:
        raise HTTPException(status_code=409, detail="Class is full")

    # Decrement available spots
    gym_class.spots_available -= 1

    booking_id = f"bk-{uuid4().hex[:8]}"

    _bookings[booking_id] = {
        "booking_id": booking_id,
        "class_id": request.class_id,
        "class_name": gym_class.name,
        "date": request.date,
        "time": gym_class.time,
        "instructor": gym_class.instructor,
        "status": "confirmed",
    }

    return BookingResponse(
        booking_id=booking_id,
        status="confirmed",
        class_info=BookingClassInfo(
            name=gym_class.name,
            time=gym_class.time,
            instructor=gym_class.instructor,
        ),
        date=request.date,
    )


@router.get("/bookings", response_model=BookingsListResponse)
async def list_bookings() -> BookingsListResponse:
    """List all bookings."""
    items = [
        BookingListItem(
            booking_id=b["booking_id"],
            class_id=b["class_id"],
            class_name=b["class_name"],
            date=b["date"],
            time=b["time"],
            status=b["status"],
        )
        for b in _bookings.values()
        if b["status"] == "confirmed"
    ]
    return BookingsListResponse(bookings=items)


@router.delete("/bookings/{booking_id}", response_model=CancelResponse)
async def cancel_booking(booking_id: str) -> CancelResponse:
    """Cancel a booking."""
    if booking_id not in _bookings:
        raise HTTPException(status_code=404, detail=f"Booking '{booking_id}' not found")

    booking = _bookings[booking_id]

    # Guard against double-cancel
    if booking["status"] == "cancelled":
        raise HTTPException(status_code=400, detail="Booking already cancelled")

    booking["status"] = "cancelled"

    # Restore the spot
    gym_class = _classes_by_id.get(booking["class_id"])
    if gym_class:
        gym_class.spots_available += 1

    return CancelResponse(status="cancelled", refund_status="processed")
