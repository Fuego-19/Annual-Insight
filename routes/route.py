from fastapi import APIRouter
from models.profDetails import profDetail
from config.database import collection_name
from schema.schema import list_serial
from bson import ObjectId
from fastapi import HTTPException


router = APIRouter()


@router.get("/")
async def get_profDetails():
    try:
        ProfDetails = list_serial(collection_name.find())
        print("dsfdsf ",collection_name.find())
        return ProfDetails
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/addProfile")
async def add_profDetails(profDetail: profDetail):
    collection_name.insert_one(dict(profDetail))