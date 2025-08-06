from fastapi import APIRouter, HTTPException, Query
from typing import List
from datetime import datetime
import pytz

from app.models import ClassOut, BookingRequest, BookingOut
from app.database import conn, cursor

router = APIRouter()

# Set timezone to IST
IST = pytz.timezone("Asia/Kolkata")


# ──────────────────────────────────────────────
# GET /classes → List all upcoming fitness classes
# ──────────────────────────────────────────────
@router.get("/classes", response_model=List[ClassOut])
def get_classes():
    cursor.execute("SELECT * FROM classes")
    rows = cursor.fetchall()
    return [
        {
            "id": row[0],
            "name": row[1],
            "datetime": datetime.fromisoformat(row[2]),
            "instructor": row[3],
            "slots": row[4]
        }
        for row in rows
    ]


# ──────────────────────────────────────────────
# POST /book → Book a class if slots available
# ──────────────────────────────────────────────
@router.post("/book", response_model=BookingOut)
def book_class(booking: BookingRequest):
    # 1. Check if class exists
    cursor.execute("SELECT * FROM classes WHERE id = ?", (booking.class_id,))
    class_row = cursor.fetchone()
    if not class_row:
        raise HTTPException(status_code=404, detail="Class not found")

    available_slots = class_row[4]
    if available_slots <= 0:
        raise HTTPException(status_code=400, detail="No slots available")

    # 2. Insert booking
    cursor.execute(
        "INSERT INTO bookings (class_id, client_name, client_email) VALUES (?, ?, ?)",
        (booking.class_id, booking.client_name, booking.client_email)
    )
    booking_id = cursor.lastrowid

    # 3. Decrease slot count
    cursor.execute(
        "UPDATE classes SET slots = slots - 1 WHERE id = ?",
        (booking.class_id,)
    )
    conn.commit()

    # 4. Return booking details
    return {
        "id": booking_id,
        "class_id": booking.class_id,
        "client_name": booking.client_name,
        "client_email": booking.client_email
    }


# ──────────────────────────────────────────────
# GET /bookings → Show bookings for an email address
# ──────────────────────────────────────────────
@router.get("/bookings", response_model=List[BookingOut])
def get_bookings(client_email: str = Query(...)):
    cursor.execute(
        "SELECT * FROM bookings WHERE client_email = ?", (client_email,))
    rows = cursor.fetchall()

    return [
        {
            "id": row[0],
            "class_id": row[1],
            "client_name": row[2],
            "client_email": row[3]
        }
        for row in rows
    ]
