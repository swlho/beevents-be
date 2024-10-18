from fastapi import FastAPI, Request, HTTPException, Header
from app.webhook_util import fulfill_checkout
import stripe

app = FastAPI()

# Use the secret provided by Stripe CLI for local testing
# or your webhook endpoint's secret.
endpoint_secret = 'whsec_...'

@app.post("/webhook")
async def stripe_webhook(request: Request, stripe_signature: str = Header(None)):
    payload = await request.body()
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, stripe_signature, endpoint_secret
        )
    except ValueError:
        # Invalid payload
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        raise HTTPException(status_code=400, detail="Invalid signature")

    if (
        event['type'] == 'checkout.session.completed'
        or event['type'] == 'checkout.session.async_payment_succeeded'
    ):
        fulfill_checkout(event['data']['object']['id'])

    return {"status": "success"}
