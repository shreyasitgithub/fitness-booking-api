from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="🏋️‍♀️ Fitness Booking API",
    description="Simple API to manage class bookings at a fitness studio.",
    version="1.0.0"
)

app.include_router(router)
