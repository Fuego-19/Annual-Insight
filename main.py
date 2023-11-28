from fastapi import FastAPI
from pymongo.mongo_client import MongoClient
from routes.route import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # You might want to specify the HTTP methods your frontend uses
    allow_headers=["*"],  # You might want to specify the headers your frontend uses
)
app.include_router(router)