from fastapi import FastAPI
from .routes.user_routes import router as UserRouter

app = FastAPI()

# Routes
app.include_router(UserRouter, tags=['user'], prefix='/user')