from fastapi import FastAPI

from .routers import enid


app = FastAPI()

app.include_router(enid.router)