from pydantic import BaseModel

class User(BaseModel):
    first_name: str
    last_name: str
    password: str
    email: str


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