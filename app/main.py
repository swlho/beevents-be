from fastapi import FastAPI
from .routes.user_routes import router as UserRouter
from .routes.events_routes import router as EventsRouter
from .routes.webhooks_routes import router as WebhooksRouter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins='*',
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

# ROUTES
# User
app.include_router(UserRouter, tags=['user'], prefix='/user')
# Events
app.include_router(EventsRouter, tags=['events'], prefix='/events')
# Webhooks
app.include_router(WebhooksRouter, tags=['webhooks'], prefix='/webhooks')