import stripe

# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
stripe.api_key = 'sk_test_51QAtGcQ8rOVglOIGT1bbRnBDynnCahoAykQV6ZFuapan0Nf21bFASXPDPfJQryCsOcWavmyd85I8ZKhUOtXIHZsl00yCHrWyZe'

def fulfill_checkout(session_id)
  print("Fulfilling Checkout Session", session_id)

  # TODO: Make this function safe to run multiple times,
  # even concurrently, with the same session ID

  # TODO: Make sure fulfillment hasn't already been
  # peformed for this Checkout Session

  # Retrieve the Checkout Session from the API with line_items expanded
  checkout_session = stripe.checkout.Session.retrieve(
    session_id,
    expand=['line_items'],
  )

  # Check the Checkout Session's payment_status property
  # to determine if fulfillment should be peformed
  if checkout_session.payment_status != 'unpaid':
    # TODO: Perform fulfillment of the line items

    # TODO: Record/save fulfillment status for this
    # Checkout Session