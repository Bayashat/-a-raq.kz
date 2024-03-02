from fastapi import FastAPI
from app.api.views import auth, shanyraks

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(shanyraks.router, prefix="/shanyraks", tags=["shanyraks"])
