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

#BOOK OR CANCEL EVENT BOOKING BY USER ID
@router.patch("/{user_id}/events/{event_id}")
def patch_book_event_by_id(user_id:str, event_id:int, response: Response, book: Union[bool, None] = None):
    try:
        events = supabase.from_("bookings")\
        .select("event_id")\
        .eq("user_id", user_id)\
        .execute()
        
        if(events):
            eventsArr = events.data
            for event in eventsArr:
                if(event_id is event["event_id"] and book is True):
                    response.status_code = status.HTTP_400_BAD_REQUEST
                    return {"message":"You are already booked into this event", "status code": response.status_code}
            
            if(book is True):
                data = supabase.from_("bookings")\
                .insert({"event_id":event_id, "user_id": user_id})\
                .execute()

                if(response):
                    response.status_code = status.HTTP_200_OK
                    return {"message":"Booking successful", "status code": response.status_code}
                
            if(book is False):
                data = supabase.from_("bookings")\
                .delete()\
                .eq("user_id", user_id)\
                .eq("event_id", event_id)\
                .execute()
                if(response):
                    response.status_code = status.HTTP_200_OK
                    return {"message":"Booking cancellation successful", "status code": response.status_code}
                    
    except Exception as e:
        print(f"Error: {e}")
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Booking cancellation failed"}

#PATCH USER'S ARCHIVED EVENTS (DELETE FROM USER'S ARCHIVED EVENTS)    
@router.patch("/{user_id}/archived-events/{event_id}")
def patch_archived_event_by_id(user_id:str, event_id:int, response: Response):
    try:
        archivedEventsArr = supabase.from_("profiles")\
        .select("archived_events")\
        .eq("id",user_id)\
        .execute()
        if(archivedEventsArr):
            patchArchivedEventsArr = archivedEventsArr.data[0]["archived_events"]
            patchArchivedEventsArr.remove(event_id)
            patch = supabase.from_("profiles")\
            .update({"archived_events": patchArchivedEventsArr})\
            .eq("id", user_id)\
            .execute()
            if(patch):
                response.status_code = status.HTTP_200_OK
                return {"message":"Delete archived event successful", "status code": response.status_code, "updated archived events": patchArchivedEventsArr}
    except Exception as e:
        print(f"Error: {e}")
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Delete archived event failed"}
    

# PATCH USER'S EVENT BY ID - ARCHIVE/UNARCHIVE EVENT
@router.patch("/{user_id}/archive/{event_id}")
def patch_toggle_archive_event(user_id:str, event_id: int, response: Response, archive: Union[bool, None] = None):
    try:
        if(archive is True):
            data = supabase.from_("bookings")\
            .update({"user_archived": True})\
            .eq("user_id", user_id)\
            .eq("event_id", event_id)\
            .execute()

            if(data):
                response.status_code = status.HTTP_200_OK
                return {"message":"Event archiving successful", "status code": response.status_code}

        if(archive is False):
            data = supabase.from_("bookings")\
            .update({"user_archived": False})\
            .eq("user_id", user_id)\
            .eq("event_id", event_id)\
            .execute()

            if(data):
                response.status_code = status.HTTP_200_OK
                return {"message":"Event unarchiving successful", "status code": response.status_code}

    except Exception as e:
        print(f"Error: {e}")
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Event update failed"}