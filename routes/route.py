from fastapi import APIRouter
from models.models import profDetail, researchContributions
from config.database import prof_collection, research_collection
from schema.schema import research_contributions_list_serial,list_serial
from bson import ObjectId
from fastapi import HTTPException
import requests
from reportlab.platypus import Image
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from fastapi.responses import FileResponse  
from reportlab.lib.colors import cyan
from datetime import date
import textwrap


from fastapi import APIRouter, HTTPException, Query
from datetime import datetime
from models.models import researchContributions
from bson import ObjectId

router = APIRouter()

@router.get("/publicationsByYear")
async def get_publications_by_year(year: int = Query(..., title="Publication Year")):
    try:
        # Convert the year to a datetime object for comparison
        year_start = datetime(year, 1, 1)
        year_end = datetime(year, 12, 31)
        
        # Query the database for publications within the specified year
        publications = research_contributions_list_serial(
            research_collection.find({
                "dateOfPublication": {
                    "$gte": year_start,
                    "$lte": year_end
                }
            })
        )
        
        return publications
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/publicationsByCoauthor")
async def get_publications_by_coauthor(coauthor_name: str = Query(..., title="Co-Author Name")):
    try:
        # Query the database for publications where the coAuthors list contains the specified co-author name
        publications = research_contributions_list_serial(
            research_collection.find({
                "coAuthors.name": {
                    "$regex": coauthor_name,
                    "$options": "i"  # "i" makes the search case-insensitive
                }
            })
        )

        return publications
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/publicationsByCoauthorAndYear")
async def get_publications_by_coauthor_and_year(
    year: int = Query(..., title="Publication Year"),
    coauthor_name: str = Query(..., title="Co-Author Name")
):
    try:
        # Convert the year to a datetime object for comparison
        year_start = datetime(year, 1, 1)
        year_end = datetime(year, 12, 31)
        
        # Query the database for publications where the coAuthors list contains the specified co-author name
        # and the publication date is within the specified year
        publications = research_contributions_list_serial(
            research_collection.find({
                "coAuthors.name": {
                    "$regex": coauthor_name,
                    "$options": "i"  # Make the search case-insensitive
                },
                "dateOfPublication": {
                    "$gte": year_start,
                    "$lte": year_end
                }
            })
        )
        
        return publications
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
    
    
    
@router.get("/publications-by-coauthor-role")
async def get_publications_by_coauthor_role(
    coauthor_role: str = Query(..., title="Co-Author Role")
):
    try:
        # Query the database for publications where the coAuthors list contains a co-author with the specified role
        publications = research_contributions_list_serial(
            research_collection.find({
                "coAuthors.role": {
                    "$regex": coauthor_role,
                    "$options": "i"  # Make the search case-insensitive
                }
            })
        )

        return publications
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
    
teal_color = (63/255, 173/255, 168/255)

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
    print("hi")
    print(researchContributions)
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






def get_current_academic_year():
    today = date.today()
    current_year = today.year
    if today.month < 8:  # Academic year starts in August
        start_year = current_year - 1
    else:
        start_year = current_year
    end_year = start_year + 1

    academic_year_string = f"Academic Year: {start_year}-{end_year}"
    return academic_year_string

def changeFontToCyan(c):
      # RGB values for #3FADA8
    c.setFillColorRGB(*teal_color)
    c.setFont("Helvetica-Bold", 14)
    

    
def changeFontToBlack(c):
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica", 10)


def get_publications_in_date_range(research_contributions, start_date, end_date):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    
    publications_in_range = []
    
    for contribution in research_contributions:
        if start_date <= contribution["dateOfPublication"] <= end_date:
            publications_in_range.append(contribution)
    
    return publications_in_range


@router.post("/test")
async def test():
    try:
        researchDetails = research_contributions_list_serial(research_collection.find())
        #print(get_publications_in_date_range(researchDetails,"2022-05-01","2023-04-30"))
        return get_publications_in_date_range(researchDetails,"2022-05-01","2023-04-30")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
    
    
def generate_publication_time_period(start_date_time, end_date_time):
    # Convert the input date-time strings to datetime objects
   
    # Define month names for formatting
    month_names = ["January", "February", "March", "April", "May", "June", "July",
                   "August", "September", "October", "November", "December"]
    
    # Format the start and end dates
    start_month_name = month_names[start_date_time.month - 1]
    end_month_name = month_names[end_date_time.month - 1]
    start_date_str = f"{start_month_name} {start_date_time.day}, {start_date_time.year}"
    end_date_str = f"{end_month_name} {end_date_time.day}, {end_date_time.year}"
    
    # Generate the publication time period string
    publication_time_period = f"(PUBLISHED BETWEEN {start_date_str.upper()} AND {end_date_str.upper()})"
    
    return publication_time_period

def generate_pdf(prof_detail, research_contributions, pdf_filename):
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    print("prof_da:", prof_detail)
    
    prof_data = prof_detail[0]
    research_data = research_contributions[0]
    
   
    c.setFont("Helvetica", 12)
    print("gg")
    # Academic Year and Professor's Name
    
    top_pos = 750
    left_pos = 80
    copy_top_pos = top_pos
    academic_year = f"{get_current_academic_year()}, {prof_data['name']}"
    c.drawString(left_pos, top_pos, academic_year)
    
    
    logo_url = "https://i.ibb.co/dmNNpc0/IIITD-Email-Footer.png"
    response = requests.get(logo_url)
    if response.status_code == 200:
        logo_image = Image(BytesIO(response.content))
        logo_image.drawHeight = 30  # Set the height of the logo image
        logo_image.drawWidth = 100   # Set the width of the logo image
        logo_image.wrapOn(c, 100, 90)  # Wrap the image to a specific size
        logo_image.drawOn(c, 400, 740)  # Position the image to the right of the heading

    
    changeFontToCyan(c)
    detail_title = "Details about the faculty member"
    c.drawString(left_pos, top_pos-20, detail_title)
    
    changeFontToBlack(c)

    # PhD Year
    phd_year = f"PhD (Year): {prof_data['phdYear']}"
    top_pos = top_pos-50
    c.drawString(left_pos, top_pos , phd_year)

    # Date of Joining
    date_of_joining = f"Date of Joining IIIT-Delhi: {prof_data['dateOfJoining']}"
    top_pos = top_pos-15
    c.drawString(left_pos, top_pos, date_of_joining)

    # Primary Department
    primary_dept = f"Primary Department: {prof_data['primaryDept']}"
    top_pos = top_pos-15
    c.drawString(left_pos, top_pos, primary_dept)

    # Broad Research Domain
   
    c.setFont("Helvetica-Bold", 10)  # Set the font to bold
    research_domain_label = "Broad Research Domain:"
    top_pos = top_pos-15
    c.drawString(left_pos, top_pos, research_domain_label)  
    string_res = ", ".join(prof_data["BroadRsrchDomain"])
    c.drawString(left_pos+125, top_pos, string_res)

    c.setFont("Helvetica", 10)  # Reset the font to regular
    
    top_pos = top_pos-30
    c.line(left_pos, top_pos, 550, top_pos) #breakline
    
   
    
    if(research_data):
        changeFontToCyan(c)
        top_pos = top_pos-20
        
        research_heading = "Research Contributions (Research, Development and Innovation)"
        c.drawString(left_pos, top_pos, research_heading)
        
        top_pos = top_pos-15
        c.setFont("Helvetica", 10)
        publication_heading = "Publications"
        c.drawString(left_pos, top_pos, publication_heading)
        
        changeFontToBlack(c)
        top_pos = top_pos-20
        c.setFont("Helvetica-Bold", 10)
        note_heading = "Full-length Journal Papers"
        c.drawString(left_pos, top_pos, note_heading)
        
        top_pos = top_pos - 20

        datesList = ["2021-05-01", "2022-05-01","2023-05-01","2024-05-01" ]
        datesList1 = ["2022-05-01", "2023-05-01","2024-05-01","2025-05-01" ]
        
        data = []
        for i in range(len(datesList)):
            time_period = get_publications_in_date_range(research_data,datesList[i],datesList1[i])
            data.append(time_period)
        
        
                
        # changeFontToBlack(c)
        # c.drawString(left_pos, top_pos, time_period)
        
        top_pos = top_pos - 20

        title =  ", ".join(research_data["coAuthors"]) + ". "+ research_data["title"]
        title = textwrap.wrap(title, width=80)  # Adjust width as needed
        print(title)
        # Print each line of the note
        for i in title:
            c.drawString(left_pos+30, top_pos, i)
            top_pos = top_pos - 15  # Decrease top_pos for the next line
        
        
        
        
    # Save the PDF
    c.save()