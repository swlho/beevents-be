from pydantic import BaseModel, EmailStr
from typing import Optional, List

class UpdateUserModel(BaseModel):
    full_name: Optional[str]



class Event(BaseModel):
    staff_id: int
    title: str
    date_time: str
    details: str
    location: str
    tags: list
    users_attending: list
    is_archived: bool
    cost: int