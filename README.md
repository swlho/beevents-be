# Beevents Backend

## Summary

This repo is the backend code of Beevents, a platform for creating and booking events.  The backend is written in Python and utilises the FastAPI library to communicate with a Supabase postgres database instance and serve data to the frontend.  The backend also hooks into the Stripe API to perform services like creating payment links, payment sessions, and verifying payments using webhooks.

#### Tech stack:

* FastAPI (Python library) server hooked to a Supabase postgres instance for the backend database, and Stripe API for payments services.

## Live Demo

You can access the live demo of the project [here](https://beevents.vercel.app/).

## Frontend Repository

You can find the frontend repository [here](https://github.com/swlho/beevents-fe).

## Getting Started

To configure this project locally, please follow these steps:

### Prerequisites

* Python (minimum version: v3)
* Node (minimum version: v20)
* Supabase postgres database project instance and api key - refer to Supabase documentation on how to do this
* Stripe API account with own API key and a created webhook for 'checkout session' - refer to Stripe documentation on how to do this

### Installation for local development

**1. Clone the repository:**

```
git clone https://github.com/swlho/beevents-be
```

2. Create the virtual environment file:

```
python3 -m venv .env
source env/bin/activate
```

**2. Install dependencies:**

```
pip install -r requirements.txt
```

**3. Create config file:**

In the project root folder, create a file 'config.py', and populate it with the following key/values, replacing the values with your own instances (n.b. values are strings):

```
url = <SUPABASE PROJECT URL>
api = <SUPABASE API KEY>
stripe_api_key = <STRIPE API KEY>
webhook_secret = <STRIPE WEBHOOK SECRET>
```

**4. Run the project locally:**

```
uvicorn app.main:app --host 0.0.0.0 --port 10000 --reload
```

This will start the local development server, which can be accessed via the terminal. This will show as: <http://0.0.0.0:10000>

## Using the Beevents app
Refer to the README located in the [Beevents frontend repo.](https://github.com/swlho/beevents-fe)