from fastapi import APIRouter, FastAPI, Request, HTTPException, Header
from config import webhook_secret
import stripe

router = APIRouter()
webhook_secret: str = webhook_secret

@router.post("/checkout-complete")
async def stripe_webhook(
    event: dict,
    request: Request,
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
        print('Succesful checkout')

    return 200
