from fastapi import APIRouter, FastAPI, Request, status, HTTPException, Header, Response
from config import webhook_secret
import stripe

from db.supabase import create_supabase_client

router = APIRouter()
webhook_secret: str = webhook_secret

# Initialize supabase client
supabase = create_supabase_client()

@router.post("/checkout-complete")
async def stripe_webhook(
    event: dict,
    request: Request,
    response: Response,
    stripe_signature=Header(None),
):
    raw_body = await request.body()

    try:
        event = stripe.Webhook.construct_event(
            payload=raw_body,
            sig_header=stripe_signature,
            secret=webhook_secret,
        )
    except Exception as e:
        raise HTTPException(422, detail=str(e))

    data = event["data"]["object"]
    if event["type"] == "checkout.session.completed":
        # your custom function to run after a successful payment

        event_id = data.metadata["event_id"]
        user_id = data.metadata["user_id"]

        booking = supabase.from_("bookings")\
        .insert({"event_id":event_id, "user_id": user_id, "paid": True})\
        .execute()

        if(booking):
            response.status_code = status.HTTP_200_OK
            return {"message":"Booking successful", "status code": response.status_code, "booking": booking}

    return 200
