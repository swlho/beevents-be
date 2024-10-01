from pydantic import BaseModel

class User(BaseModel):
    first_name: str
    last_name: str
    password: str
    email: str


class Event(BaseModel):
    title: str
    date_time: str
    details: str
    location: str
    map_data: str
    tags: list
    users_attending: list
    is_archived: bool
    cost: int
    total_revenue: int