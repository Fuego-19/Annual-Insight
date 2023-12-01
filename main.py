from fastapi import FastAPI
from pymongo.mongo_client import MongoClient
from routes.route import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)