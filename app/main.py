from fastapi import FastAPI
from app.api.views import auth

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])