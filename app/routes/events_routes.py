from fastapi import APIRouter
from db.supabase import create_supabase_client
from app.models import Event
#fn dependencies
import bcrypt

# Initialize supabase client
supabase = create_supabase_client()

# Initialize the router object
router = APIRouter()

# def event_exists(key: str = "title", value: str = None):
#     event = supabase.from_("events").select("*").eq(key, value).execute()
#     return len(event.data) > 0

# POST NEW EVENT
@router.post("/")
def create_event(event: Event):
    try:
        # event_title = event.title
        # # Check if event already exists
        # if event_exists(value=event_title):
        #     return {"message": "Event already exists"}

        # Add user to users table
        event = supabase.from_("events")\
            .insert({"title": event.title, "date_time": event.date_time, "details": event.details, "location": event.location, "map_data": event.map_data, "tags": event.tags, "users_attending": event.users_attending, "is_archived": event.is_archived, "cost": event.cost, "total_revenue": event.total_revenue}).execute()

        # Check if user was added
        if event:
            return {"message": "Event created successfully"}
        else:
            return {"message": "Event creation failed"}
    except Exception as e:
        print("Error: ", e)
        return {"message": "Event creation failed"}