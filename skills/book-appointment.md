---
description: A skill to let your LLM book gym appointments and classes
---

# Book Appointment Skill

## When to use this skill

Use this skill when the user wants to:
- Book a spot in a gym class
- Schedule a personal training session
- Reserve gym equipment or facilities
- Cancel an existing booking

## Prerequisites

This skill requires user authentication. The user must be logged in and have a valid session token.

## API Endpoints

### POST /api/bookings

Create a new booking.

**Request:**
```json
{
  "class_id": "yoga-101",
  "date": "2024-01-15"
}
```

**Response:**
```json
{
  "booking_id": "bk-12345",
  "status": "confirmed",
  "class": {
    "name": "Morning Yoga",
    "time": "07:00",
    "instructor": "Sarah"
  },
  "date": "2024-01-15"
}
```

### GET /api/bookings

List the user's current bookings.

### DELETE /api/bookings/{booking_id}

Cancel a booking.

**Response:**
```json
{
  "status": "cancelled",
  "refund_status": "processed"
}
```

## Instructions

1. **To book a class:**
   - First use the class-schedule skill to find available classes
   - Confirm the class_id and date with the user
   - Call `POST /api/bookings` with the class_id and date
   - Confirm the booking to the user

2. **To view bookings:**
   - Call `GET /api/bookings`
   - Display upcoming bookings in a clear format

3. **To cancel:**
   - First show the user their bookings via `GET /api/bookings`
   - Confirm which booking to cancel
   - Call `DELETE /api/bookings/{booking_id}`
   - Confirm cancellation and any refund status

## Example Usage

**User**: "Book me into the Monday morning yoga class"

**Steps**:
1. Call class-schedule skill to find Monday yoga classes
2. Identify the class_id (e.g., "yoga-101")
3. Confirm with user: "I found Morning Yoga at 07:00 with Sarah. Book this for Monday?"
4. On confirmation, call `POST /api/bookings` with class_id and date
5. Respond: "✅ Booked! Morning Yoga on Monday at 07:00. Booking ID: bk-12345"

## Error Handling

- **409 Conflict**: Class is full. Suggest alternatives.
- **401 Unauthorized**: User needs to log in first.
- **400 Bad Request**: Invalid class_id or date format.
