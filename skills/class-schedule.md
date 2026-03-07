---
name: mygym-class-schedule
description: A skill to let your LLM see the current gym class schedule
---

# Class Schedule Skill

## When to use this skill

Use this skill when the user wants to:
- View the gym class schedule
- Check what classes are available today or this week
- See class times and instructors
- Find a specific type of class (yoga, spinning, etc.)

## API Endpoints

### GET /api/classes

Returns the full class schedule.

**Response:**
```json
{
  "classes": [
    {
      "id": "yoga-101",
      "name": "Morning Yoga",
      "instructor": "Sarah",
      "time": "07:00",
      "duration_minutes": 60,
      "room": "Studio A",
      "spots_available": 5,
      "days": ["Monday", "Wednesday", "Friday"]
    }
  ]
}
```

### GET /api/classes?day={day}

Filter classes by day of the week.

### GET /api/classes?type={type}

Filter classes by type (yoga, spinning, strength, cardio, etc.)

## Instructions

1. Call `GET /api/classes` to retrieve the schedule
2. Parse the JSON response
3. Format the schedule in a readable table or list for the user
4. If the user asked about specific days or class types, filter accordingly
5. Highlight classes with available spots if the user seems interested in booking

## Example Usage

**User**: "What yoga classes are available this week?"

**Action**: Call `GET /api/classes?type=yoga`

**Response format**:
```
🧘 Yoga Classes This Week:

| Day       | Time  | Class          | Instructor | Spots |
|-----------|-------|----------------|------------|-------|
| Monday    | 07:00 | Morning Yoga   | Sarah      | 5     |
| Wednesday | 07:00 | Morning Yoga   | Sarah      | 3     |
| Friday    | 18:00 | Evening Flow   | Mike       | 8     |
```
