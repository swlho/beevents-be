from fastapi import FastAPI
from .routes.user_routes import router as UserRouter
from .routes.events_routes import router as EventsRouter

app = FastAPI()

# ROUTES
# User
app.include_router(UserRouter, tags=['user'], prefix='/user')
# Events
app.include_router(EventsRouter, tags=['events'], prefix='/events')