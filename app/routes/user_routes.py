import datetime
import os
from typing import Union
from fastapi import APIRouter, Body, Response, status
from app.models import UpdateUserModel
from db.supabase import create_supabase_client
#fn dependencies
import bcrypt
import stripe
from config import stripe_api_key

stripe.api_key = stripe_api_key

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
                .select("id", "updated_at", "full_name", "email")\
                .eq("id", user_id)\
                .execute()

            if user:
                return user
    except Exception as e:
        print(f"Error: {e}")
        response.status_code = status.HTTP_204_NO_CONTENT
        return {"message": "User ID not found"}
    
#PATCH USER'S NAME BY ID
@router.patch("/{user_id}")
def patch_user(user_id: str, response: Response, request: UpdateUserModel = Body(...)):
    request = {k:v for k,v in request.model_dump().items() if v is not None}
    date_time_now = datetime.datetime.now().replace(microsecond=0).isoformat()
    try:
        if user_exists("id", user_id):
            if 'full_name' in request.keys():
                user = supabase.from_("profiles")\
                .update({'full_name':request['full_name'], 'updated_at': date_time_now})\
                .eq("id", user_id)\
                .execute()
                if user:
                    response.status_code = status.HTTP_200_OK
                    return {"message": "User profile updated successfully", "status_code":response.status_code, "updated_user_data": user.data}
    except Exception as e:
        print(f"Error: {e}")
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "User profile update failed"}

#BOOK OR CANCEL EVENT BOOKING BY USER ID
@router.patch("/{user_id}/events/{event_id}")
def patch_book_event_by_id(user_id:str, event_id:int, response: Response, book: Union[bool, None] = None, cost: Union[int, None] = None):
    if cost == 0:
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
                
            if(book is False):
                data = supabase.from_("bookings")\
                .delete()\
                .eq("user_id", user_id)\
                .eq("event_id", event_id)\
                .execute()
                if(data):
                    response.status_code = status.HTTP_200_OK
                    return {"message":"Booking cancellation successful", "status code": response.status_code}

            if(book is True):
                data = supabase.from_("bookings")\
                .insert({"event_id":event_id, "user_id": user_id})\
                .execute()

            if(data):
                response.status_code = status.HTTP_200_OK
                return {"message":"Booking successful", "status code": response.status_code}
                        
        except Exception as e:
            print(f"Error: {e}")
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"message": "Something happened. Please try again"}
    
    if cost > 0:
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
            
            if(book is False):
                data = supabase.from_("bookings")\
                .delete()\
                .eq("user_id", user_id)\
                .eq("event_id", event_id)\
                .execute()
                if(response):
                    response.status_code = status.HTTP_200_OK
                    return {"message":"Booking cancellation successful", "status code": response.status_code}
        
            if(book is True):
                price_id = supabase.from_("events")\
                .select("price_id")\
                .eq("event_id", event_id)\
                .execute()

                domain_url = "https://beevents.vercel.app"
                patchPriceId = price_id.data[0]["price_id"]

                checkout_session = stripe.checkout.Session.create(
                    line_items=[{
                        'price': patchPriceId,
                        'quantity': 1,
                    }],
                    metadata={
                        "user_id": user_id,
                        "event_id": event_id,
                        "cost": cost,
                    },
                    mode='payment',
                    success_url = domain_url +'/success',
                    cancel_url = domain_url +'/',
                )
                response.status_code = status.HTTP_303_SEE_OTHER
                return {"url":checkout_session.url, "status_code":response.status_code}
            
        except Exception as e:
            print(f"Error: {e}")
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"message": "Something happened. Please try again"}
        

#DELETE FROM USER'S ARCHIVED EVENTS
@router.delete("/{user_id}/archived-events/{event_id}")
def delete_archived_event_by_id(user_id:str, event_id:int, response: Response):
    try:
        data = supabase.from_("bookings")\
        .delete()\
        .eq("user_id",user_id)\
        .eq("event_id", event_id)\
        .eq("user_archived", True)\
        .execute()
            
        if(data):
            response.status_code = status.HTTP_200_OK
            return {"message":"Delete archived event successful", "status code": response.status_code}
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