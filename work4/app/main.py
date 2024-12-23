from fastapi import FastAPI
from . import auth
from fastapi import FastAPI
from app.auth.auth import router as auth_router
from app.auth.router import router as router_router
app = FastAPI()

app.include_router(auth_router)
app.include_router(router_router)

