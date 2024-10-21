from typing import Union
from fastapi import APIRouter, Response, status
from db.supabase import create_supabase_client
from app.models import Event
#fn dependencies
import bcrypt

# Initialize supabase client
supabase = create_supabase_client()

# Initialize the router object
router = APIRouter()

def event_exists(key: str = "title", value: str = None):
    event = supabase.from_("events").select("*").eq(key, value).execute()
    return len(event.data) > 0

# POST NEW EVENT
@router.post("/")
def create_event(event: Event, response: Response):
    try:
        event_id = supabase.from_("events")\
            .select("event_id")
        # # Check if event already exists
        if event_exists(value=event_id):
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"message": "Event already exists"}

        # Add event to events table
        event = supabase.from_("events")\
            .insert({"staff_id": event.staff_id, "title": event.title, "date_time": event.date_time, "details": event.details, "location": event.location, "tags": event.tags, "users_attending": event.users_attending, "is_archived": event.is_archived, "cost": event.cost})\
            .execute()

        # Check if event was added
        if event:
            response_event = supabase.from_("events")\
            .select("event_id","staff_id", "title", "date_time", "details", "location", "tags", "users_attending", "is_archived", "cost")\
            .eq("event_id", event.data[0]["event_id"])\
            .execute()
            response.status_code = status.HTTP_201_CREATED
            return {"message": "Event created successfully", "status_code": response.status_code, "created_event": response_event}
        else:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"message": "Event creation failed"}
    except Exception as e:
        print("Error: ", e)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Event creation failed"}
    
# GET ALL EVENTS
@router.get("/")
def get_event(response: Response, event_id: Union[str, None] = None, is_archived: Union[bool, None] = None):
    try:
        events = supabase.from_("events")\
            .select("event_id", "title", "date_time", "details", "location", "tags", "cost", "is_archived")\
            .eq("is_archived", is_archived)\
            .execute()
        if events:
            return events
    except Exception as e:
        print(f"Error: {e}")
        response.status_code = status.HTTP_204_NO_CONTENT
        return {"message": "Events not found"}

#GET EVENT BY ID
@router.get("/{event_id}")
def get_event_by_id(response: Response, event_id: Union[str, None] = None):
    try:
        if event_id:
            event = supabase.from_("events")\
                .select("event_id", "title", "date_time", "details", "location", "tags", "cost", "is_archived")\
                .eq("event_id", event_id)\
                .execute()

            if event:
                return event
    except Exception as e:
        print(f"Error: {e}")
        response.status_code = status.HTTP_204_NO_CONTENT
        return {"message": "Event ID not found"}
    
#GET EVENTS BY STAFF ID
@router.get("/staff/{staff_id}")
def get_event_by_staff_id(response: Response, staff_id: Union[str, None] = None, is_archived: Union[bool, None] = None):
    try:
        if staff_id:
            events = supabase.from_("events")\
                .select("event_id", "title", "date_time", "details", "location", "tags", "cost", "is_archived")\
                .eq("staff_id", staff_id)\
                .eq("is_archived", is_archived)\
                .execute()

            if events:
                return events
    except Exception as e:
        print(f"Error: {e}")
        response.status_code = status.HTTP_204_NO_CONTENT
        return {"message": "Staff ID not found"}
    
#GET ACTIVE EVENTS BY USER ID
@router.get("/user/{user_id}")
def get_event_by_user_id(response: Response, user_id: Union[str, None] = None, is_archived: Union[bool, None] = None):
    try:
        if user_id and is_archived == False:
            user_events_arr_data = supabase.from_("bookings")\
            .select("event_id")\
            .eq("user_id", user_id)\
            .eq("user_archived", False)\
            .execute()
        
            if user_events_arr_data:
                events = []
                for event_id in user_events_arr_data.data:
                    event = supabase.from_("events")\
                    .select("event_id", "title", "date_time", "details", "location", "tags", "cost", "is_archived")\
                    .eq("event_id", event_id["event_id"])\
                    .eq("is_archived", False)\
                    .execute()
                    if(event.data):
                        events.append(event)
                return events
            
        if user_id and is_archived == True:            
            user_events_arr_data = supabase.from_("bookings")\
            .select("event_id")\
            .eq("user_id", user_id)\
            .eq("user_archived", True)\
            .execute()
        
            if user_events_arr_data:
                print(user_events_arr_data)
                events=[]
                for event_id in user_events_arr_data.data:
                    event = supabase.from_("events")\
                    .select("event_id", "title", "date_time", "details", "location", "tags", "cost", "is_archived")\
                    .eq("event_id", event_id["event_id"])\
                    .eq("is_archived", False)\
                    .execute()
                    if(event.data):
                        events.append(event)
                return events
                
    except Exception as e:
        print(f"Error: {e}")
        response.status_code = status.HTTP_204_NO_CONTENT
        return {"message": "User is not attending any events"}
    
# DELETE AN EVENT BY EVENT_ID
@router.delete("/{event_id}")
def delete_event_by_id(event_id: str, response: Response):
    try:        
        # Check if event exists
        if event_exists("event_id", event_id):
            # Delete event
            supabase.from_("events")\
                .delete().eq("event_id", event_id)\
                .execute()
            return {"message": "Event deleted successfully"}

        else:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"message": "Event deletion failed"}
    except Exception as e:
        print(f"Error: {e}")
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Event deletion failed"}

# PATCH EVENT BY ID - ARCHIVE/UNARCHIVE EVENT
@router.patch("/{event_id}")
def update_event(event_id: str, response: Response, is_archived: Union[bool, None] = None):
    try:
        # Check if event exists
        if event_exists("event_id", event_id):
            # Update event
            event = supabase.from_("events")\
            .update({"is_archived": is_archived})\
            .eq("event_id", event_id).execute()
            if event and event.data[0]["is_archived"] == True:
                response.status_code = status.HTTP_200_OK
                return {"message": "Event archived successfully", "status_code":response.status_code, "event": event.data}
            elif event and event.data[0]["is_archived"] == False:
                response.status_code = status.HTTP_200_OK
                return {"message": "Event unarchived successfully", "status_code":response.status_code, "event": event.data}
        else:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"message": "Event update failed"}
    except Exception as e:
        print(f"Error: {e}")
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Event update failed"}
    
#PATCH EVENT BY ID - ADD STRIPE PAYMENT LINK
@router.patch("/url/{event_id}/{payment_url}")
def update_event_paymenturl(event_id:str, payment_url:str, response: Response):
    try:
        # Check if event exists
        if event_exists("event_id", event_id):
            patchUrl = payment_url
            url = supabase.from_("events")\
            .update({"payment_url": patchUrl})\
            .eq("event_id", event_id)\
            .execute()
            if url:
                response.status_code = status.HTTP_200_OK
                return {"message": "Event payment url added successfully", "status_code":response.status_code, "data":{"event_id":event_id, "payment_url": payment_url}}
    except Exception as e:
        print(f"Error: {e}")
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Updating event payment url failed"}