from typing import Union
from fastapi import APIRouter, Response, status
from db.supabase import create_supabase_client
#fn dependencies
import bcrypt

# Initialize supabase client
supabase = create_supabase_client()

# Initialize the router object
router = APIRouter()

def user_exists(key: str = "email", value: str = None):
    user = supabase.from_("profiles").select("*").eq(key, value).execute()
    return len(user.data) > 0

@router.get("/{user_id}")
def get_user_by_id(response: Response, user_id: Union[str, None] = None):
    try:
        if user_id:
            user = supabase.from_("profiles")\
                .select("id", "updated_at", "full_name", "email", "events_attending", "archived_events")\
                .eq("id", user_id)\
                .execute()

            if user:
                return user
    except Exception as e:
        print(f"Error: {e}")
        response.status_code = status.HTTP_204_NO_CONTENT
        return {"message": "User ID not found"}
    
@router.patch("/{user_id}/events/{event_id}")
def patch_booked_event_by_id(user_id:str, event_id:int, response: Response):
    try:
        eventsArr = supabase.from_("profiles")\
        .select("events_attending")\
        .eq("id",user_id)\
        .execute()
        if(eventsArr):
            patchEventsArr = eventsArr.data[0]["events_attending"]
            patchEventsArr.remove(event_id)
            patch = supabase.from_("profiles")\
            .update({"events_attending": patchEventsArr})\
            .eq("id", user_id)\
            .execute()
            if(patch):
                response.status_code = status.HTTP_200_OK
                return {"message":"Booking cancellation successful", "status code": response.status_code, "updated booked events": patchEventsArr}
    except Exception as e:
        print(f"Error: {e}")
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Booking cancellation failed"}