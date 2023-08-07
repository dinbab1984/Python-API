from fastapi import FastAPI
from .routers import customers, users, login
from . import models


app = FastAPI()
app.include_router(customers.router)
app.include_router(users.router)
app.include_router(login.router)

@app.get("/")
def root():
    return {"message" : "Hello World!"}
