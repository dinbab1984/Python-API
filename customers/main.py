from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
from .routers import customers, users, login
from . import models


app = FastAPI()
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
app.include_router(users.router)
app.include_router(login.router)
app.include_router(customers.router)

@app.get("/")
def root():
    return {"message" : "Hello World!"}
