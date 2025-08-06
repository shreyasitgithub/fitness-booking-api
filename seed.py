from database import cursor, conn
from datetime import datetime, timedelta
import pytz

IST = pytz.timezone('Asia/Kolkata')

# Sample fitness classes (in IST timezone)
classes = [
    {
        "name": "Yoga",
        "datetime": IST.localize(datetime.now() + timedelta(days=1, hours=7)),  # Tomorrow 7AM IST
        "instructor": "Asha",
        "slots": 10
    },
    {
        "name": "Zumba",
        "datetime": IST.localize(datetime.now() + timedelta(days=1, hours=18)),  # Tomorrow 6PM IST
        "instructor": "Rahul",
        "slots": 15
    },
    {
        "name": "HIIT",
        "datetime": IST.localize(datetime.now() + timedelta(days=2, hours=8)),  # Day after tomorrow 8AM IST
        "instructor": "Sneha",
        "slots": 12
    }
]

# Insert into DB
for cls in classes:
    cursor.execute(
        "INSERT INTO classes (name, datetime, instructor, slots) VALUES (?, ?, ?, ?)",
        (cls["name"], cls["datetime"].isoformat(), cls["instructor"], cls["slots"])
    )

conn.commit()
print("Sample fitness classes seeded successfully!")
