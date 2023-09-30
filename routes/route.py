from fastapi import APIRouter
from models.models import profDetail, researchContributions
from config.database import prof_collection, research_collection
from schema.schema import research_contributions_list_serial,list_serial
from bson import ObjectId
from fastapi import HTTPException

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from fastapi.responses import FileResponse  

router = APIRouter()


@router.get("/")
async def get_profDetails():
    try:
        ProfDetails = list_serial(prof_collection.find())
        return ProfDetails
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/addProfile")
async def add_profDetails(profDetail: profDetail):
    prof_collection.insert_one(dict(profDetail))

@router.post("/addResearchContributions")
async def add_researchContributions(researchContributions: researchContributions):
    research_collection.insert_one(dict(researchContributions))

@router.get("/getAllContributions")
async def get_all_contributions():
    try:
        researchDetails = research_contributions_list_serial(research_collection.find())
        return researchDetails
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/generatePDF")
async def generate_pdf_endpoint(data: dict):
    try:
        prof_detail_data = list_serial(prof_collection.find())
        print("prof", prof_detail_data)
        research_contributions_data = research_contributions_list_serial(research_collection.find())
        pdf_filename = f"{prof_detail_data[0]['name']}_report.pdf"

        generate_pdf(prof_detail_data, research_contributions_data, pdf_filename)

        return FileResponse(pdf_filename, headers={"Content-Disposition": f"attachment; filename={pdf_filename}"})
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


def generate_pdf(prof_detail, research_contributions, pdf_filename):
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    print("prof_da:", prof_detail)
    c.drawString(100, 750, f"Academic Year: {prof_detail[0]['phdYear']}, {prof_detail[0]['name']}")

    c.save()