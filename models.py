from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List

class ClassOut(BaseModel):
    id: int
    name: str
    datetime: datetime
    instructor: str
    slots: int

class BookingRequest(BaseModel):
    class_id: int
    client_name: str
    client_email: EmailStr

class BookingOut(BaseModel):
    id: int
    class_id: int
    client_name: str
    client_email: EmailStr
